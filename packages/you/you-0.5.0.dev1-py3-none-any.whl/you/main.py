
import argparse
import logging
import os

from .utils.config import create_config_home, load_config, load_config_all
from .utils.logging import get_logger, init_logging, stop_logging
from .utils.python_compat import HAS_PARSE_INTERMIXED_ARGS
from .version import NAME, DESCRIPTION, __version__


LOG = get_logger(__name__)


# workaround: (for python < 3.7)
# subclass ArgumentParser so that we can handle intermixed args without error
class GoodArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        if HAS_PARSE_INTERMIXED_ARGS:
            return super(GoodArgumentParser, self).parse_args(args, namespace)
        else:
            return self.parse_known_args(args, namespace)


def get_args():
    """Parse command-line options via argparse, and return the arguments."""

    parser = GoodArgumentParser(
        prog=NAME,
        description=_(DESCRIPTION),
        epilog=_('''report bugs to: /dev/null'''),
        fromfile_prefix_chars='@')

    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__),
                        help=_('show version and exit'))

    parser.add_argument('--no-init',
                        action='store_true',
                        help=_('do not load any configuration file'))

    parser.add_argument('--config-home',
                        metavar='PATH',
                        help=_('specify config home path'))

    # parser.add_argument('-o', '--output',
    #                     metavar='FILENAME',
    #                     help=_(''))

    # [TODO] more options

    loglevel_group = parser.add_mutually_exclusive_group()
    loglevel_group.add_argument('--log',
                                choices=['DEBUG',
                                         'INFO',
                                         'WARNING',
                                         'ERROR',
                                         'CRITICAL'],
                                default='WARNING',  # default logging level
                                help=_('set logging level '
                                       '(default: WARNING)'))
    loglevel_group.add_argument('--loglevel',
                                type=int,
                                help=_('set logging level by numeric value ('
                                       '10 - DEBUG; '
                                       '20 - INFO; '
                                       '30 - WARNING; '
                                       '40 - ERROR; '
                                       '50 - CRITICAL; '
                                       '>50 - no logging)'))
    loglevel_group.add_argument('-d', '--debug',
                                action='store_true',
                                help=_('show everything, '
                                       'including debugging information '
                                       '(equivalent to: --log DEBUG)'))
    loglevel_group.add_argument('-v', '--verbose',
                                action='store_true',
                                help=_('show verbose logging '
                                       '(equivalent to: --log INFO)'))
    loglevel_group.add_argument('-q', '--quiet',
                                action='store_true',
                                help=_('silent mode, disable all logging'))

    parser.add_argument('verb',
                        nargs='?',
                        metavar='VERB',
                        help=_(''))

    parser.add_argument('objectives',
                        nargs='*',
                        metavar='OBJECTIVE',
                        help=_(''))

    if HAS_PARSE_INTERMIXED_ARGS:
        args = parser.parse_intermixed_args()
    else:  # python < 3.7
        args, argv = parser.parse_args()
        if argv:
            args.objectives += argv

    return args


def args_to_conf(args):
    """Return the configuration based on arguments."""

    conf = {}

    if args.loglevel:
        conf['loglevel'] = args.loglevel
    elif args.debug:
        conf['loglevel'] = logging.DEBUG
    elif args.verbose:
        conf['loglevel'] = logging.INFO
    elif args.quiet:
        conf['loglevel'] = logging.CRITICAL + 1
    else:  # default logging level
        conf['loglevel'] = getattr(logging, args.log.upper())

    return conf


def main():

    args = get_args()  # first!

    # for debugging load_config_all() and args_to_conf(), add:
    # init_logging(0)  # [DEBUG]
    conf = {}
    if not args.no_init:
        if args.config_home:  # load from specified config home
            conf_filename = '{}/init.py'.format(args.config_home)
            if os.path.isfile(conf_filename):
                conf.update(load_config(conf_filename))
        else:
            conf.update(load_config_all(NAME))
    conf.update(args_to_conf(args))

    # start logging in the specified level
    init_logging(conf.get('loglevel', logging.WARNING))

    # set config home and family
    if conf.get('config_home') is None:
        if conf.get('_filename'):
            conf['config_home'] = os.path.dirname(conf.get('_filename'))
        else:  # no conf file is loaded
            conf['config_home'] = create_config_home(NAME)
            # [TODO] configurationless run
    # set special fields (as absolute paths) for future use
    conf['_config_home'] = os.path.abspath(conf['config_home'])
    conf['_plugin_dir'] = os.path.join(conf['_config_home'], 'plumbus')
    conf['_profile_dir'] = os.path.join(conf['_config_home'], 'profiles')
    conf['_chrome_user_data_dir'] = os.path.join(conf['_config_home'],
                                                 'chrome_user_data')
    # [TODO] configurable plugin_dir, profile_dir, chrome_user_data_dir

    LOG.d('arguments: {}'.format(args))
    LOG.d('config: {}'.format(conf))

    # [TODO]
    print(args.verb)
    print(args.objectives)

    stop_logging()

    return 0
