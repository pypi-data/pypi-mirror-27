
from sys import version_info


# argparse doesn't allow optionals within positionals
# See also: <https://bugs.python.org/issue14191>
HAS_PARSE_INTERMIXED_ARGS = True if version_info[:2] >= (3, 7) else False
