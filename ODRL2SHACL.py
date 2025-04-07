from rdflib import Graph, Namespace, URIRef, BNode
import time
import json
from pyshacl import validate
from rdflib.plugin import PluginException

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SH = Namespace("http://www.w3.org/ns/shacl#")
malformed_feature_error_explanation = (" Accepted ODRL properties must be blank nodes with an rdf:value property, "
                                       "and an optional list of refinements (with a left operand, operator and right "
                                       "operand specified for each refinement. Please refer to the ODRL specification "
                                       "for examples.")
shape_prefixes = """@prefix dash: <http://datashapes.org/dash#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.ex/> .
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .

"""
odrl_feature_list = ["action","target","assignee","assigner","purpose"]

odrl_rule_dict={
    "P": "odrl:permission",
    "F": "odrl:prohibition",
    "O": "odrl:obligation"

}

rdf_formats = ['json-ld', 'turtle', 'xml', 'nt', 'n3', 'trig', 'nquads']

conflict_messages_req_cons = [
    'The Requester asks for permission, but there is no permission from the Provider that covers everything the Requester asks for.', # 1
    'The Requester asks for permission for something that is entirely or in part forbidden by the Provider.', #2
    'The Requester is committing to doing something that is forbidden, entirely or in part, by the Provider.', #3
    'The Requester is committing to doing something that is not explicitly permitted by the Provider.', #4
    'The Requester is not explicitly agreeing to a complete prohibition set by the Provider. ', #5
    'The Requester is not explicitly agreeing to a complete obligation set by the Provider.', #6
]
conflict_messages_any = [
    'One policy asks for permission, but there is no permission from the other policy that covers everything the first one asks for.', # 1
    'One policy asks for permission for something that is entirely or in part forbidden by the the other one.', #2
    'One policy is committing to doing something that is forbidden, entirely or in part, by the other policy.', #3
    'One policy is committing to doing something that is not explicitly permitted by the other one.', #4
    'One policy is not explicitly agreeing to a complete prohibition set by the the other one. ', #5
    'One policy is not explicitly agreeing to a complete obligation set by the other one.', #6
]
# Utility functions
mint_uri_namespace = "https://eu-upcast.github.io/shapes/mint#"
mint_uri_counter =  0
def mint_uri(tag = ""):
    global mint_uri_counter
    mint_uri_counter += 1
    return mint_uri_namespace+str(mint_uri_counter)+tag+(str(time.time()).replace(".", ""))
def tab(n):
    return " " * (2 * n)
def replace_last_semicolon(s):
    parts = s.rsplit(";", 1)  # Split from the right, at most once
    return ".".join(parts)

# this ensure that properties such as action and target are not defined directly as an IRI, but instead as a blank node
# with an rdf:value tag
def standardise_graph(graph):
    for feature in odrl_feature_list:
        prop = ODRL[feature]
        for s, p, o in graph.triples((None, prop, None)):
            if isinstance(o, URIRef):
                # Remove the old triple
                graph.remove((s, p, o))
                # Create a blank node with rdf:value
                b = BNode()
                graph.add((s, p, b))
                graph.add((b, RDF.value, o))
    return graph

# exists is a boolean, it is 1 if it should create an exists or not-exists rule
# type should be one of the following strings
# "P" for permissions
# "F" for prohibitions
# "O" for obligations
# rule_object should be the object detailing the rule to configure this shape with
def create_shape(exists, type, rule_object, message = None):
    main_shape_uri = mint_uri()
    shacl_string = "<"+main_shape_uri+"> a sh:PropertyShape  ;\n"
    #todo extend to include also the implied subjects of odrl:permission, odrl:prohibition and odrl:obligation
    if exists:
        shacl_string += tab(1)+"sh:targetClass odrl:Policy ;\n"
    if message:
        shacl_string += tab(2) + "sh:message \"\"\""+message+"\"\"\";\n"
    if len(odrl_feature_list) > 0:
        shacl_string += tab(2) + "sh:path " + odrl_rule_dict[type] + " ; \n"
        shacl_string += tab(2) + "sh:qualifiedValueShape [ \n"
        shacl_string += tab(3) + "a sh:NodeShape ; \n"
        for odrl_feature in odrl_feature_list:
            if exists:
                # check for a matching rule which is at least as general
                shacl_string += tab(3) + "sh:node [ \n"
                #shacl_string += tab(3) + "sh:path [(]sh:ZeroOrOnePath) ; \n"
                shacl_string += tab(4) + "sh:or ( \n"
                if rule_object[odrl_feature]:
                    # either the feature exists with the same parameters
                    shacl_string += tab(5) + "[ \n"
                    shacl_string += tab(6) + "sh:path ( odrl:"+odrl_feature+" rdf:value ) ; \n"
                    shacl_string += tab(6) + "sh:hasValue <" + str(rule_object[odrl_feature]["value"]) + "> ; \n"
                    shacl_string += tab(5) + "] \n"
                # or the property is not set at all (in which case it covers all possible values)
                shacl_string += tab(5) + "[ \n"
                shacl_string += tab(6) + "sh:path ( odrl:"+odrl_feature+" rdf:value ) ; \n"
                shacl_string += tab(6) + "sh:maxCount 0 ; \n"
                shacl_string += tab(5) + "] \n"
                shacl_string += tab(4) + ")  \n"
                shacl_string += tab(3) + "] ;  \n"
            elif rule_object[odrl_feature]:
                # check for a matching rule which is at least as general
                shacl_string += tab(3) + "sh:node [ \n"
                # shacl_string += tab(3) + "sh:path [(]sh:ZeroOrOnePath) ; \n"
                shacl_string += tab(4) + "sh:or ( \n"
                # either the feature exists with the same parameters
                shacl_string += tab(5) + "[ \n"
                shacl_string += tab(6) + "sh:path ( odrl:" + odrl_feature + " rdf:value ) ; \n"
                shacl_string += tab(6) + "sh:hasValue <" + str(rule_object[odrl_feature]["value"]) + "> ; \n"
                shacl_string += tab(5) + "] \n"
                # or the property is not set at all (in which case it covers all possible values)
                shacl_string += tab(5) + "[ \n"
                shacl_string += tab(6) + "sh:path ( odrl:" + odrl_feature + " rdf:value ) ; \n"
                shacl_string += tab(6) + "sh:maxCount 0 ; \n"
                shacl_string += tab(5) + "] \n"
                shacl_string += tab(4) + ")  \n"
                shacl_string += tab(3) + "] ;  \n"
                # in case we are checking for non-existence, and no feature is specified, then there will be a conflict
                # regardless of how this feature is set, and so there is nothing to check

    shacl_string += tab(2) + "] ;  \n"
    shacl_string += tab(2) + "sh:qualifiedMinCount 1 . \n"
    shacl_string += tab(1) + "\n"

    if not exists:
        second_shape_uri = mint_uri()
        shacl_string += "<" + second_shape_uri + "> a sh:NodeShape ;\n"
        shacl_string += tab(1)+"sh:targetClass odrl:Policy ;\n"
        shacl_string += tab(1) + "sh:not <"+main_shape_uri+"> .\n\n"

    return shacl_string


# Role should be "requester", "provider" or "any"
# conflict_case_selection, if different than None, it only checks one of the six conflict cases
def convert_to_shacl(graph, role = "any", conflict_case_selection = None):
    shacl_string = shape_prefixes+"\n"
    for permission in graph.objects(subject=None, predicate=ODRL.permission):
        shacl_string = shacl_string+process_rule("P", role, graph, permission, conflict_case_selection)
    for prohibition in graph.objects(subject=None, predicate=ODRL.prohibition):
        shacl_string = shacl_string+process_rule("F", role, graph, prohibition, conflict_case_selection)
    for obligation in graph.objects(subject=None, predicate=ODRL.obligation):
        shacl_string = shacl_string+process_rule("O", role, graph, obligation, conflict_case_selection)
    return shacl_string

def process_constraint_triple(graph, constraint):
    lo = next(graph.objects(subject=constraint, predicate=ODRL.leftOperand), None)
    o = next(graph.objects(subject=constraint, predicate=ODRL.operator), None)
    ro = next(graph.objects(subject=constraint, predicate=ODRL.rightOperand), None)
    if not (lo and o and ro):
        raise Exception(
            "ERROR: The refinement does not have all three of the following: left operand, operator, right "
            "operand." + malformed_feature_error_explanation)
    return {"lo": lo, "o": o, "ro": ro}

# type should be one of the following strings
# "P" for permissions
# "F" for prohibitions
# "O" for obligations
def process_constraint(type, role, graph, feature, constraint_predicate):
    refinement_object = []
    refinement_node = next(graph.objects(subject=feature, predicate=constraint_predicate), None)
    if refinement_node:
        for refinement in graph.objects(subject=refinement_node, predicate=getattr(ODRL, "and")):
            refinement_object.append(process_constraint_triple(graph, refinement))
        if len(refinement_object) == 0:
            refinement_object.append(process_constraint_triple(graph, refinement_node))
    return refinement_object

# type should be one of the following strings
# "P" for permissions
# "F" for prohibitions
# "O" for obligations
def process_rule(type, role, graph, rule, conflict_case_selection):

    shape_string = ""
    # Extract the type and optional constraints of the features
    rule_obj = {}
    for odrl_feature in odrl_feature_list:
        feature = next(graph.objects(subject=rule, predicate=getattr(ODRL, odrl_feature)), None)
        features_value = None
        feature_refinements = []
        if feature:
            features_value = next(graph.objects(subject=feature, predicate=RDF.value), None)
            if features_value == None:
                raise Exception("ERROR: "+odrl_feature+" is not defined with an rdf:value property."+malformed_feature_error_explanation)
            rule_obj[odrl_feature] = {}
            rule_obj[odrl_feature]["value"] = features_value
            rule_obj[odrl_feature]["refinements"] = process_constraint(type, role, graph, feature, ODRL.refinement)
        else:
            rule_obj[odrl_feature] = None
    if rule_obj[odrl_feature]:
        rule_obj[odrl_feature]["constraints"] = process_constraint(type, role, graph, rule, ODRL.constraint)
    rule_string = odrl_rule_dict[type] +" "+ str(rule_obj)
    if role == "requester" or role == "any":
        if type == "P":
            # Conflict case 1) Requester asks for permission, but there’s no permission from the provider that covers
            # everything the requester asks for.
            if(conflict_case_selection == 1 or conflict_case_selection == None):
                shape_string += create_shape(1, "P", rule_obj, message=rule_string)
            # Conflict case 2) Requester asks for permission for something that is entirely or in part forbidden by
            # the provider.
            if(conflict_case_selection == 2 or conflict_case_selection == None):
                shape_string += create_shape(0,"F",rule_obj, message=rule_string)
        if type == "O":
            # Conflict case 3) Requester is committing to doing something that is forbidden, entirely or in part, by
            # the provider.
            if(conflict_case_selection == 3 or conflict_case_selection == None):
                shape_string += create_shape(0, "F", rule_obj, message=rule_string)
            # Conflict case 4) The Requester is committing to doing something that is not explicitly permitted by
            # the provider.
            if(conflict_case_selection == 4 or conflict_case_selection == None):
                shape_string += create_shape(1, "P", rule_obj, message=rule_string)
    if role == "provider" or role == "any":
        if type == "F":
            # Conflict case 5) The requester is not explicitly agreeing to a complete prohibition set by the provider.
            if(conflict_case_selection == 5 or conflict_case_selection == None):
                shape_string += create_shape(1, "F", rule_obj, message=rule_string)
        if type == "O":
            # Conflict case 6) The requester is not explicitly agreeing to a complete obligation set by the provider.
            if(conflict_case_selection == 6 or conflict_case_selection == None):
                shape_string += create_shape(1, "O", rule_obj, message=rule_string)

    return shape_string

def validate_shacl(shapes_graph, data_graph):
    r = validate(data_graph,
                 shacl_graph=shapes_graph,
                 ont_graph=None,
                 inference=None,
                 abort_on_first=False,
                 allow_infos=False,
                 allow_warnings=False,
                 meta_shacl=False,
                 advanced=False,
                 js=False,
                 debug=False)
    conforms, results_graph, results_text = r
    return r



def parse_unknown_rdf(rdf_text: str):
    g = Graph()
    for fmt in rdf_formats:
        try:
            g.parse(data=rdf_text, format=fmt)
            return g
        except (PluginException, Exception) as e:
            continue  # Try the next format
    raise ValueError("Could not parse RDF data in any known format.")

def compare_policies_wrt_conflict_case(g_one,g_two,role_one, role_two, conflict_case):
    shacl_one = convert_to_shacl(g_one, role=role_one, conflict_case_selection=conflict_case)
    validation_result = validate_shacl(shacl_one, g_two)
    messages = []
    for result in validation_result[1].subjects(RDF.type, SH.ValidationResult):
        for msg in validation_result[1].objects(result, SH.resultMessage):
            messages.append(str(msg))
    return messages


# p_one and p_two are two rdflib graph objects representing a single ODRL policy each
# role_one and role_two are one of the following strings
# "any", "requester", "provider"
def compare_policies(p_one,p_two, p_one_role = "any", p_two_role = "any"):
    if ((p_one_role != "any") & (p_one_role != "requester") & (p_one_role != "provider")) | ((p_two_role != "any") & (p_two_role != "requester") & (p_two_role != "provider")) :
        raise ValueError("Undefined Semantics. At least one role is not set to the accepted values of 'requester', 'provider' or 'any'.")
    if (p_one_role == "any" and p_two_role != "any") | (p_one_role != "any" and p_two_role == "any"):
        raise ValueError("Undefined Semantics. One role is set to 'any', but the other one is not.")
    g_one = standardise_graph(p_one)
    g_two = standardise_graph(p_two)
    g_one_id = list(g_one.subjects(predicate=RDF.type, object=URIRef("http://www.w3.org/ns/odrl/2/Policy")))
    g_two_id = list(g_one.subjects(predicate=RDF.type, object=URIRef("http://www.w3.org/ns/odrl/2/Policy")))
    if len(g_one_id) != 1 & len(g_two_id) != 1:
        raise ValueError("One of the policies does not have an entity defined as an odrl:Policy, or it has more than 1.")
    conflict_data = {
        "conflict_status": "match",
        "p_one_id": g_one_id[0],
        "p_two_id": g_two_id[0],
        "p_one_role": p_one_role,
        "p_two_role": p_two_role,
        "conflict_set": [],
    }
    for i in range(1,7):
        rules_in_p1 = compare_policies_wrt_conflict_case(g_one, g_two, p_one_role, p_two_role, i)
        if(len(rules_in_p1) > 0):
            conflict_data["conflict_status"] = "conflict"
            conflict_data["conflict_set"].append(
                {
                    "conflicting_rules_in_p_one": rules_in_p1,
                    "conflicting_rules_in_p_two": [],
                    "conflict_explanation": conflict_messages_any[i-1] if p_one_role == "any" else conflict_messages_req_cons[i-1]
                }
            )
        rules_in_p2 = compare_policies_wrt_conflict_case(g_two, g_one, p_two_role, p_one_role, i)
        if (len(rules_in_p2) > 0):
            conflict_data["conflict_status"] = "conflict"
            conflict_data["conflict_set"].append(
                {
                    "conflicting_rules_in_p_one": [],
                    "conflicting_rules_in_p_two": rules_in_p2,
                    "conflict_explanation": conflict_messages_any[i-1] if p_one_role == "any" else
                    conflict_messages_req_cons[i + -1]
                }
            )
    return json.dumps(conflict_data, indent=2)

# p_one and p_two are two string serialisations of ODRL in one of the following formats:
# 'json-ld', 'turtle', 'xml', 'nt', 'n3', 'trig', 'nquads'
# role_one and role_two are one of the following strings
# "any", "requester", "provider"
def compare_policies_from_string(p_one,p_two, p_one_role = "any", p_two_role = "any"):
    g_one = parse_unknown_rdf(p_one)
    g_two = parse_unknown_rdf(p_two)
    return compare_policies(g_one, g_two, p_one_role, p_two_role)