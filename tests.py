import rdflib

import ODRL2SHACL
import examples


def testMatch(g_string,g2string,role_one = "any", role_two = "any"):
    graph = ODRL2SHACL.standardise_graph(rdflib.Graph().parse(data=g_string, format="turtle"))
    result = ODRL2SHACL.convert_to_shacl(graph,role_one)
    shapes_graph = rdflib.Graph().parse(data=result, format="turtle")
    data_graph = ODRL2SHACL.standardise_graph(rdflib.Graph().parse(data=g2string, format="turtle"))
    validation_result = ODRL2SHACL.validate_shacl(shapes_graph, data_graph)
    return validation_result[0]

def testMatchRequesterProvider(g_string,g2string,match):
    return match == (testMatch(g_string, g2string, role_one="requester", role_two="provider") & testMatch(g2string, g_string, role_one="provider", role_two="requester"))
def testMatchAny(g_string,g2string,match):
    return match == (testMatch(g_string, g2string, role_one="any", role_two="any") & testMatch(g2string, g_string, role_one="any", role_two="any"))

def run_tests():
    tests_passed = 0
    all_pass = True
    for instance in examples.all_ODRLs:
        match_check = testMatchAny(instance,instance,True)
        all_pass = all_pass and match_check
        if not match_check:
            print("Test failed: Match because they are identical")
        else: tests_passed += 1
    for pair in examples.matching_pairs:
        match_check = testMatchRequesterProvider(pair[0],pair[1],  True)
        all_pass = all_pass and match_check
        if not match_check:
            print("Test failed: "+pair[2])
        else:
            tests_passed += 1
    for pair in examples.conflict_pairs:
        match_check = testMatchRequesterProvider(pair[0],pair[1], False)
        all_pass = all_pass and match_check
        if not match_check:
            print("Test failed: "+pair[2])
        else:
            tests_passed += 1
    print("N. of passed tests: "+str(tests_passed))
    return all_pass
