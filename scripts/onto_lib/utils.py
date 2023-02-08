from pathlib import Path

import csv

from owlready2 import *

import pandas as pd

def create_csvs(path_dict: dict):
    for k in path_dict.keys():
        match k:
            case "node":
                with open(path_dict[k], 'w') as csvfile:
                    fieldnames = ['node_id:ID', 'descriptive_label:string[]', 'iri', ':LABEL']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
            case "rel":
                with open(path_dict[k], 'w') as csvfile:
                    fieldnames = [':START_ID', ':END_ID', ':TYPE', 'restriction', 'restriction_value', 'label']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
            case "err":
                with open(path_dict[k], 'w') as csvfile:
                    fieldnames = ['known', 'unknown', 'type_err']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()

def append_node(node, node_p:Path, *, node_type:str=''):
    '''
    input:
        node:
            case 1: owlready2.entity.ThingClass
            case 2: Type: str: node = string name
        node_p: path to node file to append node to
        onto_type: node type for and/or
    '''
    # construct node row
    if isinstance(node, owlready2.entity.ThingClass) or isinstance(node, owlready2.prop.ObjectPropertyClass) \
        | isinstance(node, owl.Thing) | isinstance(node, owl.Nothing):
        # ThingClass node
        try:
            node_label = ';'.join(node.label)
        except:
            node_label = ''
        node_line = [str(node), node_label, str(node.iri), node_type]
    elif isinstance(node, str):
        # Case: blank, and/or nodes
        node_line = [node, '', '', node_type]
    else:
        raise ValueError
    # write node to file
    with open(node_p, 'a') as f:
        node_writer = csv.writer(f, delimiter=',')
        node_writer.writerow(node_line)
        
def append_relation(rel_p: Path, source_id:str, target_id:str,
                    edge_type:str, restriction, restriction_val):
    try:
        edge_label = ';'.join(edge_type.label)
    except:
        edge_label = ''
        
    # construct relation row
    rel_line = [source_id, target_id, edge_type, restriction, restriction_val, edge_label]
    # write to file
    with open(rel_p, 'a') as f:
        rel_writer = csv.writer(f, delimiter=',')
        rel_writer.writerow(rel_line)

def create_transition(node_p, counter_dict, counter_key):
    # create node and append to file
    trans_node = f"{counter_dict['node_prefix']}_{counter_key}_{counter_dict[counter_key]}".upper()
    append_node(trans_node,node_p,node_type=counter_key.upper())
    # update counter
    counter_dict[counter_key] = counter_dict[counter_key] + 1
    return trans_node, counter_dict

def get_details_of_restriction(res):
    return res.property,res.type,res.value

def parse_logic(path_dict, unknown_node, known_node, edge_type, restriction_type, restriction_value,
                counter_dict, premature_nodes):
    match unknown_node:
        case owlready2.entity.ThingClass():
            # case: stop rule
            if unknown_node.name == "Thing":
                append_node(unknown_node,path_dict["node"],node_type="Thing")
            elif unknown_node.name == "Nothing":
                append_node(unknown_node,path_dict["node"],node_type="Nothing")
            else:
                append_node(unknown_node,path_dict["node"],node_type="Concept")

            if isinstance(known_node, str) and ("AND" in known_node or "OR" in known_node):
                # AND/OR nodes are the targets of classes in conjunctons
                append_relation(path_dict["rel"], unknown_node, known_node, edge_type, restriction_type, restriction_value)
            else:
                append_relation(path_dict["rel"], known_node, unknown_node, edge_type, restriction_type, restriction_value)
            if isinstance(known_node, str) and ("AND" in known_node or "OR" in known_node):
                # AND/OR nodes are the targets of classes in conjunctons
                append_relation(path_dict["rel"], unknown_node, known_node, edge_type, restriction_type, restriction_value)
            else:
                append_relation(path_dict["rel"], known_node, unknown_node, edge_type, restriction_type, restriction_value)
        
        case owlready2.prop.ObjectPropertyClass():
            append_node(unknown_node,path_dict["node"],node_type="Property")
            if isinstance(known_node, str) and ("AND" in known_node or "OR" in known_node):
                # AND/OR nodes are the targets of classes in conjunctons
                append_relation(path_dict["rel"], known_node, unknown_node, edge_type, restriction_type, restriction_value)
            else:
                append_relation(path_dict["rel"], unknown_node, known_node, edge_type, restriction_type, restriction_value)

        case owlready2.class_construct.And():
            ## AND Node creation
            counter_key = "and"
            trans_node, counter_dict = create_transition(path_dict["node"], counter_dict, counter_key)
            # link to known
            append_relation(path_dict["rel"], known_node, trans_node, edge_type, restriction_type, restriction_value)

            # Iterate through AND list
            for connected_node in unknown_node.is_a:
                # make recursion call on connected node
                counter_dict, premature_nodes = parse_logic(path_dict, connected_node, trans_node, "member_of",
                    restriction_type, restriction_value, counter_dict, premature_nodes)
                
        case owlready2.class_construct.Or():
            counter_key = "or"
            trans_node, counter_dict = create_transition(path_dict["node"], counter_dict, counter_key)
            # link to known
            append_relation(path_dict["rel"], known_node, trans_node, edge_type, restriction_type, restriction_value)

            # Iterate through OR list
            for connected_node in unknown_node.Classes:
                # make recursion call on connected node
                counter_dict, premature_nodes = parse_logic(path_dict, connected_node, trans_node, "member_of",
                    restriction_type, restriction_value, counter_dict, premature_nodes)

        case owlready2.class_construct.Restriction():
            ## BLANK Node Creatiom
            counter_key = "blank"
            trans_node, counter_dict = create_transition(path_dict["node"], counter_dict, counter_key)

            # make edge between known and blank
            append_relation(path_dict["rel"], trans_node, known_node, edge_type, restriction_type, restriction_value)
            
            # Get values out of restriction
            edge_label, restriction, new_unknown_type = get_details_of_restriction(unknown_node)
            restr_value = ""
            match restriction:
                case 24: # SOME
                    restriction_name = "SOME"
                case 25: # ONLY
                    restriction_name = "ONLY"
                case 26: # EXACTLY
                    restriction_name = "EXACTLY"
                    restr_value = unknown_node.cardinality
                case 27: # MIN
                    restriction_name = "MIN"
                    restr_value = unknown_node.cardinality
                case 28:
                    restriction_name = "MAX"
                    restr_value = unknown_node.cardinality
                case 29:
                    restriction_name = "VALUE"
                    restr_value = unknown_node.cardinality
                case _:
                    print(restriction)
                    print(unknown_node)
                    raise NotImplementedError

            assert isinstance(edge_label, owlready2.prop.ObjectPropertyClass) or \
                    isinstance(edge_label, owlready2.prop.DataPropertyClass), f"{edge_label} {type(edge_label)}"
            counter_dict, premature_nodes = parse_logic(path_dict, new_unknown_type, trans_node, edge_label,
                restriction_name, restr_value, counter_dict, premature_nodes)

        case owlready2.class_construct.Not():
            ## Not Node Creation
            counter_key = "not"
            trans_node, counter_dict = create_transition(path_dict["node"], counter_dict, counter_key)
            # make edge between known and blank
            append_relation(path_dict["rel"], trans_node, known_node, edge_type, restriction_type, restriction_value)
            
            # Get values out of restriction
            counter_dict, premature_nodes = parse_logic(path_dict, unknown_node.Class, trans_node, "member_of",
                restriction_type, restriction_value, counter_dict, premature_nodes)
            
        case owlready2.class_construct.OneOf():
            ## OneOf Node creation
            counter_key = "OneOf"
            trans_node, counter_dict = create_transition(path_dict["node"], counter_dict, counter_key)
            # made edge between OneOf and known
            append_relation(path_dict["rel"], known_node, trans_node, edge_type, restriction_type, restriction_value)
            
            # Iterate through AND list
            # print(unknown_node.instances)
            for connected_node in unknown_node.instances:
                # OneOf instance returns list of instances of type OneOf node
                # therefore, we need to temporarily cast connected node to type thing class
                # types.new_class(connected_node.name, (Thing,))
                
                # make recursion call on connected node
                counter_dict, premature_nodes = parse_logic(path_dict, 
                    types.new_class(connected_node.name, (Thing,)), trans_node, 
                    "member_of", restriction_type, restriction_value, counter_dict, premature_nodes)

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
            premature_nodes.add(known_node)
        case owl.Thing():
            if unknown_node.name == "Nothing":
                append_node(unknown_node,path_dict["node"],node_type="Nothing")
            else:
                append_node(unknown_node,path_dict["node"],node_type="Thing")
        case _:
            # print out type
            # print(f"node: {c} Unknown type: {type(unknown_node)} on {c.iri}")
            row = [known_node, unknown_node, type(unknown_node)]
            with open(path_dict["err"], 'a') as f:
                err_writer = csv.writer(f, delimiter=',')
                err_writer.writerow(row)
            # pass
            raise TypeError(f"Unknown type: {type(unknown_node)}")
    return counter_dict, premature_nodes

def parse_ontology(path_dict, onto, *, node_prefix="upper"):
    # create node counters
    counter_dict = {k: 0 for k in ["and", "or", "blank", "not", "OneOf"]}
    counter_dict["node_prefix"] = node_prefix

    # create nodes that might end prematurely due to badly formed concepts
    premature_nodes = set()

    # special handle owl.Thing (type: THING) and owl.Nothing (type: NOTHING)
    for c in onto.classes():
        # add class to node file
        if c.name == "Thing":
            append_node(c,path_dict["node"],node_type="Thing")
        elif c.name == "Nothing":
            append_node(c,path_dict["node"],node_type="Nothing")
        else:
            append_node(c,path_dict["node"],node_type="Concept")

        # check if equivalence is not empty
        if list(c.equivalent_to):
            for sc in c.equivalent_to:
                counter_dict, premature_nodes = parse_logic(path_dict,
                    sc, c, "equivalent_to", "", "", counter_dict, premature_nodes)
        elif list(c.is_a):
            for sc in c.is_a:
                counter_dict, premature_nodes = parse_logic(path_dict,
                    sc, c, "is_a", "", "", counter_dict, premature_nodes)
        else:
            print(f"{c} does not have equivalent_to or is_a properties.")

    for p in onto.object_properties():
        append_node(p,path_dict["node"],node_type="Property")

        # check if equivalence is not empty
        if list(p.subclasses()):
            for sp in p.subclasses():
                counter_dict, premature_nodes = parse_logic(path_dict,
                    sp, p, "subproperty_of", "", "", counter_dict, premature_nodes)

    # Clean up any issues with the csvs
    clean_csvs(path_dict, premature_nodes)

def clean_csvs(path_dict, premature_nodes):
    # load in nodes and drop duplicates
    node_df = pd.read_csv(path_dict['node'])
    node_df.drop_duplicates(subset='node_id:ID', inplace=True)

    # load in rels and drop duplicates
    rel_df = pd.read_csv(path_dict['rel'])
    rel_df.drop_duplicates(inplace=True)

    # check any iffy nodes and remove them
    for iffy_n in premature_nodes:
        m = rel_df[":START_ID"].str.contains(iffy_n) | rel_df[":END_ID"].str.contains(iffy_n)
        if m.sum() < 2:
            rel_df.drop(rel_df[m].index, inplace=True)
            n = node_df['node_id:ID'].str.contains(iffy_n)
            node_df.drop(node_df[n].index, inplace=True)

    # write cleaned csvs to file
    node_df.to_csv(path_dict['node'],index=False)
    rel_df.to_csv(path_dict['rel'],index=False)
    print(f"Final node count: {node_df.shape[0]}")
    print(f"Final rel count: {rel_df.shape[0]}")