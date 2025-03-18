import rdflib

import ODRL2SHACL
import examples


def testMatch(g_string,g2string,match):
    graph = rdflib.Graph().parse(data=g_string, format="turtle")
    result = ODRL2SHACL.convert_to_shacl(graph)
    shapes_graph = rdflib.Graph().parse(data=result, format="turtle")
    data_graph = rdflib.Graph().parse(data=g2string, format="turtle")
    validation_result = ODRL2SHACL.validate_shacl(shapes_graph, data_graph)
    return validation_result[0] == match

def run_tests():
    all_pass = True
    for pair in examples.matching_pairs:
        match_check = testMatch(pair[0],pair[1],True)
        all_pass = all_pass and match_check
        if not match_check:
            print("Test failed: "+pair[2])
    for pair in examples.conflict_pairs:
        match_check = testMatch(pair[0],pair[1],False)
        all_pass = all_pass and match_check
        if not match_check:
            print("Test failed: "+pair[2])
    return all_pass
