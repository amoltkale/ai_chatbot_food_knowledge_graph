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