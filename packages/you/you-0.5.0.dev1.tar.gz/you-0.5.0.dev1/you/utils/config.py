
import os
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
        conf['_filename'] = filename  # record filename in a special field
    else:
        LOG.w(_('failed to load config from {}: not a file').format(filename))
    return conf


def load_config_all(name):
    """Load all configuration files by program name."""

    conf = {}
    conf_filenames = []
    conf_filenames.append('/etc/{}.py'.format(name))  # system-wide

    home = environ.get('HOME')
    if home:
        conf_filenames.append('{}/.config/{}/init.py'.format(home, name))
        conf_filenames.append('{}/.{}/init.py'.format(home, name))

    xdg_config_home = environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        conf_filenames.append('{}/{}/init.py'.format(xdg_config_home, name))

    # [TODO] support Windows %LOCALAPPDATA%, %APPDATA% or %HOMEPATH%

    # special environment variable: $YOU_CONFIG_HOME
    you_config_home = environ.get('YOU_CONFIG_HOME')
    if you_config_home:
        conf_filenames.append('{}/init.py'.format(you_config_home))

    for conf_filename in conf_filenames:
        if path.isfile(conf_filename):
            conf.update(load_config(conf_filename))

    LOG.d('finished loading config: {}'.format(conf))
    return conf


def create_config_home(name):
    """Create a default config home directory by program name."""

    conf_dir = ''

    home = environ.get('HOME')
    if home:
        conf_dir = path.join(home, '.config', name)

    xdg_config_home = environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        conf_dir = path.join(xdg_config_home, name)

    # [TODO] support Windows %LOCALAPPDATA%, %APPDATA% or %HOMEPATH%

    # special environment variable: $YOU_CONFIG_HOME
    you_config_home = environ.get('YOU_CONFIG_HOME')
    if you_config_home:
        conf_dir = you_config_home

    if conf_dir == '':
        LOG.wtf(_('cannot determine config home (your OS is not supported)'))
        exit(1)

    try:
        os.makedirs(conf_dir, mode=0o755, exist_ok=True)  # python >= 3.2
    except Exception as ex:
        LOG.wtf(_('failed to create config home {}: {}').format(conf_dir, ex))
        exit(1)
    return conf_dir
