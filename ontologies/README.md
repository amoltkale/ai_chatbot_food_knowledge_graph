# onto_parser
To run: `python onto_parser.py --in_path <path to owl file>`

## How it works
load ontology
get all entities (ontology.classes())
for each entity
    for each subclass_of/equivalent_to (entity.equivalent_to OR entity.is_a returns unknown class)
        call parser(unknown_class, known_class)

def parser (recursive function)
    match type(unknown class)
        case owlready2.entity.ThingClass()
            # stop criteria
        case owlready2.prop.ObjectPropertyClass()
            # stop criteria
        case owlready2.class_construct.And()
            # creates the transition node
            # creates the edge between last known and transition<AND>
            for each clause in unknown_class<AND> (.is_a)
                call parser(clause, AND_transition)
        case owlready2.class_construct.Or()
            # similar to AND case, but owlready2 function changes
            for each clause in unknown_class<OR> (.Classes)
                call parser(clause, OR_transition)
        case owlready2.class_construct.Restriction()
            restriction type = unknown_class<Restriction>.property,unknown_class<Restriction>.type,unknown_class<Restriction>.value
            match on restriction type
            # dig deeper into types
            call parser(unknown_class<Restriction>.value, RESTRICTION_transition)
        case owlready2.class_construct.Not()
            # apple_whole(not apple_slice)
            call parser(clause) (unknown_class.Class)
        case owlready2.class_construct.OneOf()
            for each clause in unknown_class<OneOf> (.instances)
                call parser(clause, ONEOF_transition)
        case primitive type
            # track premature node ends)

### post emit fixes
remove duplicate nodes (pandas drop_duplicates)
check node list generated from primitive type match
    for each node in list
        if sum of edges coming out of node < 2
            # drop transition node relation in dataframe
            # drop node from node dataframe
write out cleaned csv

# neo4j
## import
```bash
./bin/neo4j-admin database import full --trim-strings=true neo4j \
--overwrite-destination --nodes=import/nodes.csv \
--relationships=import/rels.csv
```
## create full text index
```
CREATE FULLTEXT INDEX label_index
FOR (n:Concept)
ON EACH [n.descriptive_label]
OPTIONS {
  indexConfig: {
    `fulltext.analyzer`: 'english',
    `fulltext.eventually_consistent`: true
  }
}
```