import os
import csv
from pathlib import Path
from owlready2 import *
import pandas as pd


def get_details_of_restriction(res):
    return res.property, res.type, res.value


def create_transitionary_node(node_type, node_counter):
    # pass
    # AND_00000001
    # OR_00000001
    # BLANK_00000001

    node = f"{node_type.upper()}_{node_counter}"
    node_counter = node_counter + 1
    return node, node_counter


def append_relation(rel_path: Path, source_id: str, target_id: str,
                    edge_type: str, restriction: str = ''):
    try:
        edge_label = ';'.join(edge_type.label)
    except:
        edge_label = ''

    # construct relation row
    rel_line = [source_id, target_id, edge_type, restriction, edge_label]
    # write to file
    with open(rel_path, 'a') as f:
        rel_writer = csv.writer(f, delimiter=',')
        rel_writer.writerow(rel_line)


def append_node(node, node_path: Path, *, node_type: str = ''):
    '''
    input:
        node:
            case 1: owlready2.entity.ThingClass
            case 2: Type: str: node = string name
        node_p: path to node file to append node to
        onto_type: node type for and/or
    '''
    # construct node row
    if isinstance(node, owlready2.entity.ThingClass):
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
    with open(node_path, 'a') as f:
        node_writer = csv.writer(f, delimiter=',')
        node_writer.writerow(node_line)


def parse_logic(node_path, rel_path, unknown_node, known_node, edge_type, restriction_type, and_count, or_count, blank_count, not_count):
    match type(unknown_node):
        case owlready2.entity.ThingClass:
            # case: stop rule
            append_node(unknown_node, node_path, node_type="Concept")
            if isinstance(known_node, str) and ("AND" in known_node or "OR" in known_node):
                # AND/OR nodes are the targets of classes in conjunctons
                append_relation(rel_path, unknown_node,
                                known_node, edge_type, restriction_type)
            else:
                append_relation(rel_path, known_node,
                                unknown_node, edge_type, restriction_type)
        case owlready2.class_construct.And:
            # AND Node creation
            and_node, and_count = create_transitionary_node('AND', and_count)
            append_node(and_node, node_path, node_type='AND')
            # made edge between AND and known
            append_relation(rel_path, known_node, and_node,
                            edge_type, restriction_type)

            # Iterate through AND list
            for connected_node in unknown_node.is_a:
                # make recursion call on connected node
                and_count, or_count, blank_count, not_count = parse_logic(node_path, rel_path, connected_node, and_node, "member_of",
                                                                          restriction_type,
                                                                          and_count, or_count, blank_count, not_count)

        case owlready2.class_construct.Or:
            # AND Node creation
            or_node, or_count = create_transitionary_node('OR', or_count)
            append_node(or_node, node_path, node_type='OR')
            # made edge between OR and known
            append_relation(rel_path, known_node, or_node,
                            edge_type, restriction_type)

            # Iterate through OR list
            for connected_node in unknown_node.Classes:
                # make recursion call on connected node
                and_count, or_count, blank_count, not_count = parse_logic(node_path, rel_path, connected_node, or_node, "member_of",
                                                                          restriction_type,
                                                                          and_count, or_count, blank_count, not_count)

        case owlready2.class_construct.Restriction:
            # BLANK Node Creatiom
            blank_node, blank_count = create_transitionary_node(
                'BLANK', blank_count)
            append_node(blank_node, node_path, node_type='BLANK')
            # make edge between known and blank
            append_relation(rel_path, blank_node, known_node,
                            edge_type, restriction_type)

            # Get values out of restriction
            edge_label, restriction, new_unknown_type = get_details_of_restriction(
                unknown_node)

            match restriction:
                case 24:  # SOME
                    restriction_name = "SOME"
                case 25:  # ONLY
                    restriction_name = "ONLY"
                case 26:  # EXACTLY
                    restriction_name = "EXACTLY"
                case 27:  # MIN
                    restriction_name = "MIN"
                case 28:
                    restriction_name = "MAX"
                case 29:
                    restriction_name = "VALUE"
                case _:
                    print(restriction)
                    print(unknown_node)
                    raise NotImplementedError

            assert isinstance(edge_label, owlready2.prop.ObjectPropertyClass) or \
                isinstance(
                    edge_label, owlready2.prop.DataPropertyClass), f"{edge_label} {type(edge_label)}"
            and_count, or_count, blank_count, not_count = parse_logic(node_path, rel_path, new_unknown_type, blank_node, edge_label,
                                                                      restriction_name,
                                                                      and_count, or_count, blank_count, not_count)

        case owlready2.class_construct.Not:
            # Not Node Creatiom
            not_node, not_count = create_transitionary_node('NOT', not_count)
            append_node(not_node, node_path, node_type='NOT')
            # make edge between known and blank
            append_relation(rel_path, not_node, known_node,
                            edge_type, restriction_type)

            # Get values out of restriction
            and_count, or_count, blank_count, not_count = parse_logic(node_path, rel_path, unknown_node.Class, not_node, "member_of",
                                                                      restriction_type,
                                                                      and_count, or_count, blank_count, not_count)

        case _:
            # print out type
            raise TypeError(f"Unknown type: {unknown_node}")
    return and_count, or_count, blank_count, not_count


def parse_ontology(node_path, rel_path, onto):
    # skeleton loop
    and_count = 0
    or_count = 0
    blank_count = 0
    not_count = 0

    for c in onto.classes():
        append_node(c, node_path, node_type="Concept")

        if list(c.equivalent_to):
            for sc in c.equivalent_to:
                and_count, or_count, blank_count, not_count = parse_logic(node_path, rel_path, sc, c, "equivalent_to", "", and_count, or_count,
                                                                          blank_count, not_count)
        elif list(c.is_a):
            for sc in c.is_a:
                and_count, or_count, blank_count, not_count = parse_logic(node_path, rel_path, sc, c, "is_a", "", and_count, or_count,
                                                                          blank_count, not_count)
        else:
            print(":(")


def main():
    # create write paths
    input_data = os.listdir('data/input')
    for onto_data in input_data:
        onto_name = onto_data.split('_')[0]
        node_path = f"data/output/{onto_name}_nodes.csv"
        rel_path = f"data/output/{onto_name}_rels.csv"
        onto_file = f"data/input/{onto_name}_ontology.owl"

        print(f"Parse {onto_name}? y/n")
        response = input()

        if response == "y":
            if Path(node_path).is_file():
                print(
                    f"There exists a node and relations file for {onto_name}, are you sure you want to continue? The existing file will be deleted. y/n")
                response = input()
                if response == "y":
                    os.remove(node_path)
                    os.remove(rel_path)
                if response != "y":
                    continue

            with open(node_path, 'w') as csvfile:
                fieldnames = ['node_id:ID',
                              'descriptive_label:string[]', 'iri', ':LABEL']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

            with open(rel_path, 'w') as csvfile:
                fieldnames = [':START_ID', ':END_ID',
                              ':TYPE', 'restriction', 'label']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

            onto = get_ontology(onto_file).load()
            parse_ontology(node_path, rel_path, onto)

            node_df = pd.read_csv(node_path)
            node_df.drop_duplicates(inplace=True)
            node_df.to_csv(node_path, index=False)

            rel_df = pd.read_csv(rel_path)
            rel_df.drop_duplicates(inplace=True)
            rel_df.to_csv(rel_path, index=False)


if __name__ == "__main__":
    main()
