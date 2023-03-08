# Add annotations to concept nodes
```sql
LOAD CSV WITH HEADERS FROM 'file:///annot.csv' AS row
MATCH (n:Concept {node_id: row.node_id})
WITH n, row
CALL apoc.create.setProperty(n, row.annot_label, [x in apoc.text.split(row.annot, '###')])
YIELD node
RETURN COUNT(*)
```

# Add index on node id
```sql
CREATE TEXT INDEX node_index
FOR (n:Concept)
ON (n.node_id)
```

# Recursive Query: 2_deep_apple
```sql
MATCH p=(n)-[r]->(c)
WHERE n.iri =~ ".*FOODON_03310788.*"
WITH c
MATCH p2=(c)<-[r2 *1..2]-(other)
    WHERE LABELS(other) = ["Concept"]
RETURN p2
```

# Recursive Query: 2_deep_sausage
```sql
MATCH p=(n)-[r]->(c)
WHERE n.iri =~ ".*FOODON_00001007.*"
WITH c
MATCH p2=(c)<-[r2 *1..2]-(other)
    WHERE LABELS(other) = ["Concept"]
RETURN p2
```
# Find whole/part apple
```sql
MATCH (n:Concept)
WHERE n.iri =~ (".*FOODON_03310788.*") 
RETURN n
```

# Find not type
```sql
MATCH p=(n)-[r *1..]->(c)
WHERE n.iri =~ ".*FOODON_03310788.*"
    AND LABELS(c) <> ["AND"]
RETURN p
```

# controlled recursion for bidirection
```sql
MATCH p=(n)-[r *1..]->(c)
WHERE n.iri =~ ".*FOODON_03310788.*"
WITH c
MATCH p2=(c)<-[r2 *1..3]-(other)
RETURN p2
```

## get rid of the blank transition node
Ends on concepts
```sql
MATCH p=(n)-[r *1..]->(c)
WHERE n.iri =~ ".*FOODON_03310788.*"
WITH c
MATCH p2=(c)<-[r2 *1..]-(other)
    WHERE LABELS(other) = ["Concept"]
RETURN p2
```

### end on blank nodes
```sql
MATCH p=(n)-[r *1..]->(c)
WHERE n.iri =~ ".*FOODON_03310788.*"
WITH c
MATCH p2=(c)<-[r2 *1..]-(other)
    WHERE LABELS(other) = ["BLANK"]
RETURN p2
```

# uncontrolled recursion depth
```sql
MATCH p=(n)-[r *1..]->(c)
WHERE n.iri =~ ".*FOODON_03310788.*"
WITH c
MATCH p2=(c)<-[r2 *1..]-(other)
RETURN p2
```