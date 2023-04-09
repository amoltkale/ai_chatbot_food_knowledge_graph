from owlready2 import *
'''
Solution to making patterns:
Start each transition node with ROOT_TRANSITION
    Maintain list of transitions visited while going down path
    Append each entity name attached to transition (_ENTITY)
    ex: APPLE_AND_SLICE_BAKED
    Go through tree and write any new entity nodes to csv
        Assert that transition nodes are never seen again
        Write edges out as well
    Similar to set of entity nodes
Updating Neo4j:
    Look for new nodes
    Find all places where new node appears and update any transitions if desired
'''
class Graph:
    def __init__(self, root):
        self.root = root
        self.entity_list = [root.id]
        self.transition_list = []

class EntityNode:
    # def __init__(self, entity, neo_type, parent=None):
    def __init__(self, entity, neo_type):
        self.id = str(entity)
        self.label = ';'.join(entity.label)
        self.iri = entity.iri
        self.neo_type = neo_type
        self.children = []
        # self.parent = parent

    def add_node(self, node_obj, *, direction, rel_type):
        if direction != "source" and direction != "target":
            raise ValueError(f"direction can only be source or target, recieved {direction}")
        self.children.append({"node"     : node_obj,
                              "direction": direction,
                              "rel_type" : rel_type
                              })

class TransitionNode:
    # def __init__(self, neo_type, parent):
    def __init__(self, id, neo_type):
        self.id = id
        self.label = None
        self.iri = None
        self.neo_type = neo_type
        self.children = []
        # self.parent = parent

    def rename(self, new_id: str):
        self.id = new_id
        return self

    def add_node(self, node_obj, *, direction, rel_type):
        if direction != "source" and direction != "target":
            raise ValueError(f"direction can only be source or target, recieved {direction}")
        self.children.append({"node"     : node_obj,
                              "direction": direction,
                              "rel_type" : rel_type
                              })
