"""
Utility functions to conform to XDG's specifications
"""

import os

from mgcomm.env import var_split, home

_opj = os.path.join
_sep = os.path.sep


# TODO: windows: https://stackoverflow.com/questions/43853548/xdg-basedir-directories-for-windows
# pylint: disable=invalid-name
_ENVDIRS = {
    # name: (main, main_default, additional, additional_default)
    'cache': (
        'XDG_CACHE_HOME', _opj(home(), '.cache'), None, None),
    'config': (
        'XDG_CONFIG_HOME', _opj(home(), '.config'),
        'XDG_CONFIG_DIRS', _opj(_sep, 'etc', 'xdg')),
    'data': (
        'XDG_DATA_HOME',
        _opj(home(), '.local', 'share'),
        'XDG_DATA_DIRS',
        [_opj(_sep, 'usr', 'local', 'share'), _opj(_sep, 'usr', 'share')]),
    'runtime': (
        'XDG_RUNTIME_DIR', _opj(_sep, 'run', 'user', str(os.getuid())),
        None, None),
}


def basedir(base, *, subdir='', file=''):
    """Return a path to the first valid directory or file (if file is given)
    which follows XDG Base Directory specification.
    Returned path doesn't have to exist but it follows current user settings and
    should be used by an application to either read or write files (depending on
    current user's read-write permissions).

    Arguments:
        - base
            one of the strings: cache, config, data, runtime.
        - subdir:
            subdirectory of XDG directory which should be searched
        - file:
            file in either base directory or a given `subdir` which should be
            searched

    Examples:
        assert '/home/user/.config/app/cfg.ini' ==
                    basedir('config', subdir='app', file='cfg.ini')
        assert '/home/user/.config/cfg.ini' ==
                    basedir('config', file='cfg.ini')
        assert '/home/user/.config/app' ==
                    basedir('config', subdir='app')
    """
    base = base.lower()

    if base not in _ENVDIRS.keys():
        raise ValueError(
            "'base' should be one of %s', not %s" % (_ENVDIRS.keys(), base))

    searched = _xdg_base_dirs(*_ENVDIRS[base])
    if subdir or file:
        for bd in searched:
            search = _opj(bd, subdir, file)
            if os.path.exists(search):
                return search.rstrip(_sep)
    return _opj(searched[0], subdir, file).rstrip(_sep)


def _xdg_base_dirs(main, main_default,
                   additional=None, additional_default=None):
    main_dir = var_split(main, main_default)
    if additional:
        additional_dir = var_split(additional, additional_default)
    else:
        additional_dir = []
    return main_dir + additional_dir
