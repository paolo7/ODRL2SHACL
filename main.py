import rdflib
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, URIRef, Literal

import examples
import ODRL2SHACL
import tests


def testGraph(g_string,g2string):
    graph = rdflib.Graph().parse(data=g_string, format="turtle")
    result = ODRL2SHACL.convert_to_shacl(graph)
    print(result)
    shapes_graph = rdflib.Graph().parse(data=result, format="turtle")
    data_graph = rdflib.Graph().parse(data=g2string, format="turtle")
    validation_result = ODRL2SHACL.validate_shacl(shapes_graph, data_graph)
    print(validation_result[0])
    print(validation_result[1])
    print(validation_result[2])


print("All tests successful: "+str(tests.run_tests()))

json_result = ODRL2SHACL.compare_policies_from_string(examples.upcast_example_1_minimal,examples.upcast_example_2_minimal,"requester","provider")

print(json_result)

json_result = ODRL2SHACL.compare_policies_from_string(examples.example_12,examples.example_14,"requester","provider")

print(json_result)

json_result = ODRL2SHACL.compare_policies_from_string(examples.example_22,examples.example_19,"requester","provider")

print(json_result)

json_result = ODRL2SHACL.compare_policies_from_string(examples.example_22,examples.example_19,"any","any")

print(json_result)