from pathlib import Path

import argparse

from owlready2 import get_ontology

from onto_lib.utils import parse_ontology, create_csvs

def parse_args():
    #TODO add verbose flag and node prefix
    parser = argparse.ArgumentParser(description = 'Parse owl files into neo4j compatible csv files')
    parser.add_argument('--in_path', type=Path, help="path to ontology file")
    return parser.parse_args()

def main():
    '''
    path_dict: 3 paths: node, rel, err
    '''
    args = parse_args()

    # validate path is valid
    assert args.in_path.is_file(), f"invalid path {args.in_path}"

    # create out path and other resulting paths
    out_p = args.in_path.parent / "out"
    out_p.mkdir(exist_ok=True)

    path_dict = {"node": out_p / "nodes.csv",
                 "rel": out_p / "rels.csv",
                 "err": out_p / "error_log.csv"}

    # create csvs for neo4j
    create_csvs(path_dict)

    # load ontology
    onto = get_ontology(str(args.in_path)).load()

    # parse ontology
    parse_ontology(path_dict, onto, node_prefix="upper")

if __name__ == "__main__":
    main()