import ODRL2SHACL

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
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
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
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:create
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
  ] ;
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

upcast_example_1_minimal_single_permission = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
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
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
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
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
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

upcast_example_4_minimal = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
  ] .
"""
upcast_example_5_minimal = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:permission [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
  ] .
"""
example_6 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:prohibition [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ;
  ] .
"""
example_7 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_8 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:prohibition [
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
  ] ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_9 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:prohibition [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_10 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:prohibition [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:install
    ] ;
  ] ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_11 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:prohibition [

    odrl:action [
      rdf:value odrl:modify
    ] ;

  ] ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_12 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_13 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_14 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_15 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
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
example_16 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:prohibition [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ; 
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_17 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
    odrl:prohibition [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:install
    ] ;
  ] ;
  odrl:permission [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_18 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
      odrl:prohibition [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:install
    ] ;
  ] ;
  odrl:obligation [
    odrl:target [
      a odrl:AssetCollection ;
      rdf:value <http://example.org/datasets/covid19Stats>
    ] ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_19 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ; 
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] ;
  odrl:permission [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_20 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ; 
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_21 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_22 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ; 
    odrl:action [
      rdf:value odrl:install
    ] ;
  ] .
"""
example_23 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ; 
    odrl:assigner [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#MilitaryOrganisation>
    ] ; 
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] .
"""
example_24 = example_prefixes+"""
<"""+ODRL2SHACL.mint_uri(tag = "policy")+""">
  a odrl:Policy ;
  odrl:obligation [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:assignee [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#AcademicScientificOrganisation>
    ] ; 
    odrl:action [
      rdf:value odrl:modify
    ] ;
  ] ;
  odrl:permission [
    odrl:target <http://example.org/datasets/covid19Stats> ;
    odrl:action [
      rdf:value odrl:modify
    ] ;
    odrl:assigner [
      a odrl:PartyCollection ;
      rdf:value <https://w3id.org/dpv/owl#MilitaryOrganisation>
    ] ; 
  ] .
"""
all_ODRLs = [
    upcast_example_1_minimal,
    upcast_example_2_minimal,
    upcast_example_3_minimal,
    upcast_example_4_minimal,
    upcast_example_5_minimal,
    example_7,example_10,example_13,example_14,example_15,example_16,
]
# policies that conflict with themselves:
# example_8, example_12, example_9, example_11

matching_pairs = [
    (upcast_example_3_minimal, upcast_example_1_minimal, "Match because the second is more general (fewer permissions asked)"),
    (upcast_example_3_minimal, upcast_example_4_minimal, "Match because the second is more general (no action specified)"),
    (upcast_example_4_minimal, upcast_example_5_minimal,  "Match because the second is just a different serialisation of the first (the second does not use rdf:value in target)"),
    (upcast_example_5_minimal, upcast_example_4_minimal,  "Match because the second is just a different serialisation of the first (the first does not use rdf:value in target)"),
    (example_17, example_10, "Match because the second prohibits something that is different from what is being requested. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 2)."),
    (example_18, example_10, "Match because the second prohibits something that is different from what is being committed. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 2)."),
    (example_12, example_13, "Match because what is being obligated by the first is permitted by the second."),
    (example_12, example_14, "Match because what is being obligated by the first is permitted in an even more general way by the second."),
    (example_6, example_16, "Match because the permission of the requester is more stringent than the one of the provider."),
    (example_20, example_19, "Match because the requester commits to do what the requester asks"),
    (example_21, example_19, "Match because the requester commits to do more than what the requester asks (still within permissions)"),
]
conflict_pairs = [
    (upcast_example_1_minimal_single_permission, upcast_example_2_minimal, "Conflict because different assignee"),
    (upcast_example_1_minimal, upcast_example_3_minimal, "Conflict because the first asks for more permissions than what is offered"),
    (upcast_example_4_minimal, upcast_example_3_minimal, "Conflict because the first permission is more general (no action specified)"),
    (upcast_example_5_minimal, example_6, "Conflict because what is permitted in the first is prohibited in the second"),
    (example_7, example_8, "Conflict because what is permitted in the first is prohibited in part by the second. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 2)."),
    (example_7, example_9, "Conflict because what is permitted in the first is fully prohibited by the second. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 2)."),
    (example_7, example_11,"Conflict because what is permitted in the first is prohibited by the second with an even more general statement. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 2)."),
    (example_12, example_12, "Conflict because what is obligated in the first is not explicitly permitted by the second. (technically the requester's policy implies permission, but it is not explicit."),
    (example_12, example_8, "Conflict because what is obligated in the first is prohibited in part by the second. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 3)."),
    (example_12, example_9, "Conflict because what is obligated in the first is fully prohibited by the second. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 3)."),
    (example_12, example_11,"Conflict because what is obligated in the first is prohibited by the second with an even more general statement. (technically the requester's policy is not consistent, but this is done on purpose to highlight conflict rule 3)."),
    (example_12, example_15,"Conflict because what is obligated in the first is only partially permitted by the second."),
    (example_16, example_6, "Conflict because the permission of the requester is less stringent than the one of the provider."),
    (example_22, example_19, "Conflict because the requester does not commit to do what the provider asks (still within permissions)"),
    (example_23, example_19, "Conflict because the requester commits to something less than what the requester wants"),
    (example_23, example_24, "Conflict because the requester commits to something less than what the requester wants (the permission from the requester side should align more with the obligation)"),
]

