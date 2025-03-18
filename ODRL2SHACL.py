from pyexpat import features
from xml.sax.handler import feature_namespaces
from rdflib import Graph, Namespace, URIRef
import time
from pyshacl import validate

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

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
# Utility functions
mint_uri_namespace = "https://eu-upcast.github.io/shapes/mint#"
mint_uri_counter =  0
def mint_uri():
    global mint_uri_counter
    mint_uri_counter += 1
    return mint_uri_namespace+str(mint_uri_counter)+(str(time.time()).replace(".", ""))
def tab(n):
    return " " * (2 * n)
def replace_last_semicolon(s):
    parts = s.rsplit(";", 1)  # Split from the right, at most once
    return ".".join(parts)

# exists is a boolean, it is 1 if it should create an exists or not-exists rule
# type should be one of the following strings
# "P" for permissions
# "F" for prohibitions
# "O" for obligations
# rule_object should be the object detailing the rule to configure this shape with
def create_shape(exists, type, rule_object):
    main_shape_uri = mint_uri()
    shacl_string = "<"+main_shape_uri+"> a sh:NodeShape ;\n"
    #todo extend to include also the implied subjects of odrl:permission, odrl:prohibition and odrl:obligation
    if exists:
        shacl_string += tab(1)+"sh:targetClass odrl:Policy ;\n"
    shacl_string += tab(1) + "sh:property [ \n"
    shacl_string += tab(2) + "sh:path "+odrl_rule_dict[type]+" ; \n"
    for odrl_feature in odrl_feature_list:
        if rule_object[odrl_feature]:
            # check for a matching rule which is at least as general
            shacl_string += tab(2) + "sh:or ( \n"
            # either the feature exists with the same parameters
            shacl_string += tab(3) + "[sh:property [ \n"
            shacl_string += tab(4) + "sh:path ( odrl:"+odrl_feature+" rdf:value ) ; \n"
            shacl_string += tab(4) + "sh:hasValue <" + str(rule_object[odrl_feature]["value"]) + "> ; \n"
            shacl_string += tab(3) + "]] \n"
            # or the property is not set at all (in which case it covers all possible values)
            shacl_string += tab(3) + "[sh:property [ \n"
            shacl_string += tab(4) + "sh:path ( odrl:"+odrl_feature+" rdf:value ) ; \n"
            shacl_string += tab(4) + "sh:maxCount 0 ; \n"
            shacl_string += tab(3) + "]] \n"

            shacl_string += tab(2) + ") ; \n"
    shacl_string += tab(2) + "sh:minCount 1 ; \n"
    shacl_string += tab(1) + "] . \n\n"

    if not exists:
        second_shape_uri = mint_uri()
        shacl_string += "<" + second_shape_uri + "> a sh:NodeShape ;\n"
        shacl_string += tab(1)+"sh:targetClass odrl:Policy ;\n"
        shacl_string += tab(1) + "sh:not <"+main_shape_uri+"> .\n"

    return shacl_string

def convert_to_shacl(graph, role = "requester"):
    shacl_string = shape_prefixes+"\n"
    for permission in graph.objects(subject=None, predicate=ODRL.permission):
        shacl_string = shacl_string+process_rule("P", role, graph, permission)
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
def process_rule(type, role, graph, rule):
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

    if role == "requester":
        if type == "P":
            # Conflict case 1) Requester asks for permission, but there’s no permission from the provider that covers
            # everything the requester asks for.
            shape_string += create_shape(1, "P", rule_obj)
            # Conflict case 2) Requester asks for permission for something that is entirely or in part forbidden by
            # the provider.
            shape_string += create_shape(0,"F",rule_obj)
        if type == "O":
            # Conflict case 3) Requester is committing to doing something that is forbidden, entirely or in part, by
            # the provider.
            shape_string += create_shape(0, "F", rule_obj)
            # Conflict case 4) The Requester is committing to doing something that is not explicitly permitted by
            # the provider.
            shape_string += create_shape(1, "P", rule_obj)
    if role == "provider":
        if type == "F":
            # Conflict case 5) The requester is not explicitly agreeing to a complete prohibition set by the provider.
            shape_string += create_shape(1, "F", rule_obj)
        if type == "O":
            # Conflict case 6) The requester is not explicitly agreeing to a complete obligation set by the provider.
            shape_string += create_shape(1, "O", rule_obj)

    return shape_string
    #print(str(type)+": "+str(rule_obj))

def validate_shacl(shapes_graph, data_graph):
    r = validate(data_graph,
                 shacl_graph=shapes_graph,
                 ont_graph=None,
                 inference='rdfs',
                 abort_on_first=False,
                 allow_infos=False,
                 allow_warnings=False,
                 meta_shacl=False,
                 advanced=False,
                 js=False,
                 debug=False)
    conforms, results_graph, results_text = r
    return r