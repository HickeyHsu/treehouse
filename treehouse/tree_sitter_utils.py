from tree_sitter import Language, Parser
import os

# Language.build_library(
#     # Store the library in the `build` directory
#     "build/my-languages.so",
#     # Include one or more languages
#     ["build/tree-sitter-c",],
# )

C_LANGUAGE = Language(r"D:\python-workspace\treehouse\build\my-languages.so", "cpp")
c_parser = Parser()
c_parser.set_language(C_LANGUAGE)

