import argparse
from pathlib import Path

from owlready2 import *

import pandas as pd

from onto_lib.onto_classes import *
from onto_lib.utils import create_csvs

def parse_args():
    #TODO add verbose flag and node prefix
    parser = argparse.ArgumentParser(description = 'Parse owl files into neo4j compatible csv files')
    parser.add_argument('--in_path', type=Path, help="path to ontology file")
    return parser.parse_args()

def convert_owl(in_p:Path, out_p:Path):
    path_dict = {"node":    out_p / f"{in_p.stem}_nodes.csv",
                "rel":     out_p / f"{in_p.stem}_rels.csv",
                }
    # load ontologies
    onto = get_ontology(str(in_p)).load()
    annot_dict = initialize_annots(onto)
    create_csvs(path_dict, annot_list=list(annot_dict.keys()))

    g = create_graph(onto, path_dict)

    # verify no dups for nodes
    class_node_df = pd.read_csv(path_dict["node"])
    print(f"Node shape before: {class_node_df.shape[0]}")
    print(f"Node shape after: {class_node_df.drop_duplicates().shape[0]}")

    # verify no dups for rels
    class_rel_df = pd.read_csv(path_dict["rel"])
    print(f"Rels shape before: {class_rel_df.shape[0]}")
    print(f"Rels shape after: {class_rel_df.drop_duplicates().shape[0]}")

def main():
    '''
    path_dict: 3 paths: node, rel, err
    '''
    args = parse_args()

    # create out path and other resulting paths
    out_p = args.in_path.parent / "out"
    out_p.mkdir(exist_ok=True)

    # validate path is valid
    if args.in_path.is_dir():
        # pass
        for owl_p in args.in_path.glob('*.owl'):
            convert_owl(owl_p, out_p)
    elif args.in_path.is_file():
        assert args.in_path.suffix == ".owl", f"Must be an owl file, given {args.in_path.suffix} file"
        convert_owl(args.in_path, out_p)

if __name__ == "__main__":
    main()