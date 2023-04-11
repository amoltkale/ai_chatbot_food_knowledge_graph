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

def extract_restriction(res):
    return res.property,res.type,res.value

def parse_logic(unknown_node, known_node, *, edge, edge_direction, restr_key, restr_value):
    # TODO add flag to invalidate tree
    match unknown_node:
        case owlready2.entity.ThingClass():
            # case: stop rule
            # determine node type
            if unknown_node.name == "Thing":
                node_type = "Thing"
            elif unknown_node.name == "Nothing":
                node_type = "Nothing"
            else:
                node_type = "Concept"

            # Create node and add as child of known node
            # new_node = EntityNode(unknown_node, node_type, known_node)
            new_node = EntityNode(unknown_node, node_type)
            known_node.add_child(new_node,
                                rel_type=edge, direction=edge_direction,
                                restr_key=restr_key, restr_value=restr_value
                                )

        case owlready2.prop.ObjectPropertyClass():
            node_type = "Property"
            # Create node and add as child of known node
            # new_node = EntityNode(unknown_node, node_type, known_node)
            new_node = EntityNode(unknown_node, node_type)
            known_node.add_child(new_node,
                                rel_type=edge, direction=edge_direction,
                                restr_key=restr_key, restr_value=restr_value
                                )

        case owlready2.class_construct.And():
            # Add node
            # trans_node = TransitionNode(f"AND_{str(unknown_node)}", "AND", known_node)
            trans_node = TransitionNode(f"AND_{str(unknown_node)}", "AND")
            # link to known
            known_node.add_child(trans_node,
                    rel_type=edge, direction=edge_direction,
                    restr_key=restr_key, restr_value=restr_value
                    )

            # Iterate through AND list
            for connected_node in unknown_node.is_a:
                # make recursion call on connected node
                # connected_node will be added as child in call
                parse_logic(connected_node, trans_node,
                            edge="member_of", edge_direction="source",
                            restr_key=None, restr_value=None
                            )

        case owlready2.class_construct.Or():
            # OR node
            # trans_node = TransitionNode(f"OR_{str(unknown_node)}", "OR", known_node)
            trans_node = TransitionNode(f"OR_{str(unknown_node)}", "OR")
            # link to known
            known_node.add_child(trans_node,
                    rel_type=edge, direction=edge_direction,
                    restr_key=restr_key, restr_value=restr_value
                    )

            # Iterate through OR list
            for connected_node in unknown_node.Classes:
                # make recursion call on connected node
                # connected_node will be added as child in call
                parse_logic(connected_node, trans_node,
                            edge="member_of", edge_direction="source",
                            restr_key=None, restr_value=None
                            )

        case owlready2.class_construct.Restriction():
            # BLANK node
            # trans_node = TransitionNode(f"BLANK_{str(unknown_node)}", "BLANK", known_node)
            trans_node = TransitionNode(f"BLANK_{str(unknown_node)}", "BLANK")
            # link to known
            known_node.add_child(trans_node,
                    rel_type=edge, direction=edge_direction,
                    restr_key=restr_key, restr_value=restr_value
                    )

            # Get values out of restriction
            edge_label, restriction, new_unknown_type = extract_restriction(unknown_node)
            r_val = None
            match restriction:
                case 24: # SOME
                    r_key = "SOME"
                case 25: # ONLY
                    r_key = "ONLY"
                case 26: # EXACTLY
                    r_key = "EXACTLY"
                    r_val = unknown_node.cardinality
                case 27: # MIN
                    r_key = "MIN"
                    r_val = unknown_node.cardinality
                case 28:
                    r_key = "MAX"
                    r_val = unknown_node.cardinality
                case 29:
                    r_key = "VALUE"
                    r_val = unknown_node.cardinality
                case _:
                    print(restriction)
                    print(unknown_node)
                    raise NotImplementedError

            assert isinstance(edge_label, owlready2.prop.ObjectPropertyClass) or \
                    isinstance(edge_label, owlready2.prop.DataPropertyClass), f"{edge_label} {type(edge_label)}"

            parse_logic(new_unknown_type, trans_node,
                        edge=edge_label, edge_direction="target",
                        restr_key=r_key, restr_value=r_val
                        )

        case owlready2.class_construct.Not():
            # NOT node
            # trans_node = TransitionNode(f"NOT_{str(unknown_node)}", "NOT", known_node)
            trans_node = TransitionNode(f"NOT_{str(unknown_node)}", "NOT")

            # link to known
            known_node.add_child(trans_node,
                    rel_type=edge, direction=edge_direction,
                    restr_key=restr_key, restr_value=restr_value
                    )
            
            # Get NOT children
            parse_logic(unknown_node.Class, trans_node,
                        edge="member_of", edge_direction="source",
                        restr_key=None, restr_value=None
                        )

        case owlready2.class_construct.OneOf():
            # OneOf node
            # trans_node = TransitionNode(f"ONEOF_{str(unknown_node)}", "ONEOF", known_node)
            trans_node = TransitionNode(f"ONEOF_{str(unknown_node)}", "ONEOF")

            # link to known
            known_node.add_child(trans_node,
                    rel_type=edge, direction=edge_direction,
                    restr_key=restr_key, restr_value=restr_value
                    )
            
            # Iterate through OneOf list
            for connected_node in unknown_node.instances:
                # OneOf instance returns list of instances of type OneOf node
                # therefore, we need to temporarily cast connected node to type thing class
                # types.new_class(connected_node.name, (Thing,))
                
                # make recursion call on connected node
                parse_logic(types.new_class(connected_node.name, (Thing,)), trans_node,
                            edge="member_of", edge_direction="source",
                            restr_key=None, restr_value=None
                            )

        case type() | bool() | None:
            '''
            Tends to come from poorly defined restrictions
            Merchant Category Code -[hasMerchantCategoryDescription]->Some(str)
            Translation: Merchant category code with a valid category description of str
            example class & iri: FunctionalEntities.MerchantCategoryCode, 
            https://spec.edmcouncil.org/fibo/ontology/BE/FunctionalEntities/FunctionalEntities/MerchantCategoryCode
            Under FunctionalEntities.MerchantCategoryCode is_a:
            [ClassificationSchemes.IndustrySectorClassifier,
             LanguageRepresentation.CodeElement,
             CountryRepresentation.classifies.some(FunctionalEntities.Merchant),
             Relations.isDefinedIn.exactly(1, FunctionalEntities.MerchantCategoryCodeScheme),
             FunctionalEntities.hasMerchantCategoryDescription.some(<class 'str'>),
             LanguageRepresentation.hasTag.exactly(1, <class 'str'>)]
            '''
            pass
            # premature_nodes.add(known_node)
            # logic_pattern = None
        case owl.Thing():
            if unknown_node.name == "Nothing":
                node_type = "Nothing"
            else:
                node_type = "Thing"
            # new_node = EntityNode(unknown_node, node_type, known_node)
            new_node = EntityNode(unknown_node, node_type)
            known_node.add_child(new_node,
                                rel_type=edge, direction=edge_direction,
                                restr_key=restr_key, restr_value=restr_value
                                )
        case _:
            raise NotImplementedError
            # print out type
            # print(f"node: {c} Unknown type: {type(unknown_node)} on {c.iri}")
            # row = [known_node, unknown_node, type(unknown_node)]
            # with open(path_dict["err"], 'a') as f:
            #     err_writer = csv.writer(f, delimiter=',')
            #     err_writer.writerow(row)
            # pass
            # raise TypeError(f"Unknown type: {type(unknown_node)}")
    return


def create_graph(onto):
    entity_set = set()
    transition_set = set()
    for entity in onto.classes():
        if entity.name == "Thing":
            node_type = "Thing"
        elif entity.name == "Nothing":
            node_type = "Nothing"
        else:
            node_type = "Concept"

        # Add node and create graph
        # root_node = EntityNode(entity, node_type, None)
        root_node = EntityNode(entity, node_type)
        g = Graph(root_node, entity_set, transition_set)

        # Add children to root node
        if list(entity.equivalent_to):
            for child in entity.equivalent_to:
                parse_logic(child, root_node,
                            edge="equivalent_to", edge_direction="target",
                            restr_key=None, restr_value=None
                            )

        elif list(entity.is_a):
            for child in entity.is_a:
                parse_logic(child, root_node,
                            edge="is_a", edge_direction="target",
                            restr_key=None, restr_value=None
                            )

        else:
            print(f"{root_node.id} does not have equivalent_to or is_a properties.")

        # root_node.set_children()
    return g

class Graph:
    def __init__(self, root, entity_set, transition_set):
        self.root = root
        self.entity_set = entity_set
        self.transition_set = transition_set
        self.pattern = None

    def export_graph(self):
        raise NotImplementedError

class EntityNode:
    '''
    TODO: Generalize entire class to Node then inherient both EntityNode and TransitionNode types
    Make use of same methods for both classes
    '''
    # def __init__(self, entity, neo_type, parent=None):
    def __init__(self, entity, neo_type):
        self.entity = entity
        self.id = str(entity)
        try:
            self.label = ';'.join(entity.label)
        except:
            self.label = ""
        self.iri = entity.iri
        self.neo_type = neo_type
        self.children = []
        # self.parent = parent

    def add_child(self, node_obj, *, direction, rel_type, restr_key, restr_value):
        if direction != "source" and direction != "target":
            raise ValueError(f"direction can only be source or target, recieved {direction}")
        try:
            # Quick and dirty way
            # Can check type to do this better
            rel_label = ';'.join(rel_type.label)
        except:
            rel_label = ''
        self.children.append({"node"     : node_obj,
                              "direction": direction,
                              "rel_type" : rel_type,
                              "rel_label": rel_label,
                              "restriction": restr_key,
                              "restriction_value": restr_value
                              })

    def set_children(self):
        raise NotImplementedError

class TransitionNode:
    # def __init__(self, id, neo_type, parent=None):
    def __init__(self, id, neo_type):
        self.id = id
        self.label = None
        self.iri = None
        self.neo_type = neo_type
        self.children = []
        # self.parent = parent

    def add_child(self, node_obj, *, direction, rel_type, restr_key, restr_value):
        if direction != "source" and direction != "target":
            raise ValueError(f"direction can only be source or target, recieved {direction}")
        try:
            # Quick and dirty way
            # Can check type to do this better
            rel_label = ';'.join(rel_type.label)
        except:
            rel_label = ''
        self.children.append({"node"     : node_obj,
                              "direction": direction,
                              "rel_type" : rel_type,
                              "rel_label": rel_label,
                              "restriction": restr_key,
                              "restriction_value": restr_value
                              })

    def set_children():
        raise NotImplementedError

class BrandedFoodNode:
    def __init__(self):
        raise NotImplementedError