from os.path import dirname, join, abspath
from re import compile

this_dir = dirname(abspath(__file__))
global_config = join(this_dir, "global_config.yml")

setup_file_replacement_string = """#
# DO NOT DELETE THIS COMMENT OR CODE
with open('__version__', 'r') as f:
    version = f.read().strip()


setup("""

replace_newlines_base = "sed -i 's/\r$//' "

version_pattern = 'version\s*=\s*.+,'
version_regex = compile(version_pattern)
has_import_regex = compile("DO NOT DELETE THIS COMMENT OR CODE")
