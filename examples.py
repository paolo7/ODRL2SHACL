example_prefixes = """
@prefix dash: <http://datashapes.org/dash#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.ex/> .
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
"""

upcast_example_1 = example_prefixes+"""

<http://example.org/policy-de27e137-d0ce-4cd9-bf60-7a20afd143a3>
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      odrl:refinement [
        odrl:leftOperand <http://njh.me/QUERY> ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "Example query"^^xsd:string
      ] ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      odrl:refinement [
        odrl:leftOperand <http://njh.me/hasStartTime> ;
        odrl:operator odrl:gt ;
        odrl:rightOperand "01/05/2025"^^xsd:string
      ] ;
      rdf:value odrl:transfer
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      odrl:refinement [
        odrl:leftOperand <http://njh.me/hasName> ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "University"^^xsd:string
      ] ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
    odrl:constraint [ odrl:and [
        odrl:leftOperand odrl:purpose ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "https://w3id.org/dpv/owl#AcademicResearch"^^xsd:string
      ], [
        odrl:leftOperand <http://njh.me/hasApprovalFrom> ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "government"^^xsd:string
      ] ], [
      odrl:leftOperand odrl:spatial ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "Europe"^^xsd:string
    ] ;
  ] ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      odrl:refinement [
        odrl:leftOperand <http://njh.me/QUERY> ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "Example query"^^xsd:string
      ] ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      odrl:refinement [
        odrl:leftOperand <http://njh.me/hasStartTime> ;
        odrl:operator odrl:gt ;
        odrl:rightOperand "01/05/2025"^^xsd:string
      ] ;
      rdf:value odrl:modify
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      odrl:refinement [
        odrl:leftOperand <http://njh.me/hasName> ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "University"^^xsd:string
      ] ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
    odrl:constraint [ odrl:and [
        odrl:leftOperand odrl:purpose ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "https://w3id.org/dpv/owl#AcademicResearch"^^xsd:string
      ], [
        odrl:leftOperand <http://njh.me/hasApprovalFrom> ;
        odrl:operator odrl:eq ;
        odrl:rightOperand "government"^^xsd:string
      ] ], [
      odrl:leftOperand odrl:spatial ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "Europe"^^xsd:string
    ] ;
  ] .
"""

upcast_example_1_minimal = example_prefixes+"""

<http://example.org/policy-de27e137-d0ce-4cd9-bf60-7a20afd143a3>
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
  ] .
"""

upcast_example_2_minimal = example_prefixes+"""

<http://example.org/policy-de27e137-d0ce-4cd9-bf60-7a20afd143a3>
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#MilitaryOrganisation>
    ] ;
  ] .
"""

upcast_example_3_minimal = example_prefixes+"""

<http://example.org/policy-de27e137-d0ce-4cd9-bf60-7a20afd143a3>
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
  ] .
"""

all_ODRLs = [
    upcast_example_1_minimal,
    upcast_example_2_minimal,
    upcast_example_3_minimal,
]

matching_pairs = [
    (upcast_example_1_minimal, upcast_example_3_minimal, "Match because the second is more general"),
]
conflict_pairs = [
    (upcast_example_1_minimal, upcast_example_2_minimal, "Conflict because different assignee"),
]

