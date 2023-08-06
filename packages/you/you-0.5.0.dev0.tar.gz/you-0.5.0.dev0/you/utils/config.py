
from os import environ, path

from .logging import get_logger


LOG = get_logger(__name__)


def load_config(filename):
    """Load a configuration file by filename."""
    LOG.d('reading config from {}'.format(filename))

    conf = {}
    if path.isfile(filename):
        with open(filename) as f:
            blob = f.read()
        try:
            exec(blob)
        except Exception as ex:
            LOG.wtf(_('failed to load config from {}: {}').format(filename, ex))
            exit(1)
        temp = locals()
        for i in temp:
            if i not in ['blob', 'conf', 'f', 'filename']:
                conf[i] = temp[i]
    else:
        LOG.w(_('failed to load config from {}: not a file').format(filename))
    return conf


def load_config_all(name):
    """Load all configuration files by program name."""

    conf = {}
    conf_filenames = []
    conf_filenames.append('/etc/{}.py'.format(name))  # system-wide

    xdg_config_home = environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        conf_filenames.append('{}/{}/init.py'.format(xdg_config_home, name))

    home = environ.get('HOME')
    if home:
        conf_filenames.append('{}/.config/{}/init.py'.format(home, name))
        conf_filenames.append('{}/.{}/init.py'.format(home, name))

    # TODO: support Windows %LOCALAPPDATA%, %APPDATA% or %HOMEPATH%

    for conf_filename in conf_filenames:
        if path.isfile(conf_filename):
            conf.update(load_config(conf_filename))

    LOG.d('finished loading config: {}'.format(conf))
    return conf
