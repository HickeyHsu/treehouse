import glob
import json
from pathlib import Path
from tree_sitter_cfg.base_visitor import BaseVisitor
from tree_sitter_cfg.cfg_creator import CFGCreator
from tree_sitter_cfg.tree_sitter_utils import c_parser
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename to parse")
    parser.add_argument("--print_ast", action="store_true", help="print AST")
    parser.add_argument("--cfg", action="store_true", help="create CFG")
    parser.add_argument("--draw", action="store_true", help="draw CFG")
    parser.add_argument("--file", action="store_true", help="write CFG to file")
    args = parser.parse_args()

    args.filename = Path(args.filename)
    if args.filename.is_dir():
        filenames = list(args.filename.rglob("*.c"))
    elif args.filename.is_file():
        filenames = [args.filename]
    else:
        raise FileNotFoundError(args.filename)
    print("parsing", len(filenames), "files", filenames[:5])
    for filename in filenames:
        try:
            with open(filename, "rb") as f:
                tree = c_parser.parse(f.read())
            
            if args.print_ast:
                v = BaseVisitor()
                v.visit(tree.root_node)

            if args.cfg:
                v = CFGCreator()
                cfg = v.generate_cfg(tree.root_node)
                if args.draw:
                    print(cfg)
                    if cfg.number_of_nodes() > 1000 or cfg.number_of_edges() > 1000:
                        print("fuck man I'm not drawing that!")
                        continue
                    pos = nx.spring_layout(cfg, seed=0)
                    nx.draw(cfg, pos=pos)
                    nx.draw_networkx_labels(cfg, pos=pos, labels={n: attr.get("label", "<NO LABEL>") for n, attr in cfg.nodes(data=True)})
                    plt.show()
                if args.file:
                    for n in cfg.nodes():
                        del cfg.nodes[n]["n"]
                    with open(str(filename) + ".graph.json", "w") as of:
                        json.dump(json_graph.node_link_data(cfg, attrs=None), of, indent=2)
        except Exception:
            print("could not parse", filename)
            # raise
        print("successfully parsed", filename)
