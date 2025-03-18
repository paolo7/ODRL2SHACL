# ODRL2SHACL

Policy objects are supposed to be ODRL turtle files,
with the following restrictions:
* Each turtle file should contain a single Policy object
* It supports the following features: 
  * action
  * target
  * assignee
  * assigner
  * purpose (this is not a standard ODRL feature, but an optional addition)
* Each feature must be blank nodes with an rdf:value property, and optional refinements

Refinements and constraints are currently not supported

## Semantics

Policies are associated with 2 roles: *requester* and *provider*. 
A conflict is detected if the requester policy is not equivalent or more restrictive
than the provider one. 