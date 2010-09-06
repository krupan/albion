#! /usr/bin/env python
######################################################################
# Copyright 2010 Bryan Murdock <bmurdock@gmail.com>
#
# This file is part of albion.
#
# albion is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# albion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with albion.  If not, see <http://www.gnu.org/licenses/>.
######################################################################

import os
import sys

envs_path_var = 'ALBION_ENVS_PATH'
env_var = 'ALBION_ENV'
configs_path_var = 'ALBION_CONFIGS_PATH'
configs_loaded_var = 'ALBION_CONFIGS_LOADED'
keepers = ['COLORTERM',
           'DBUS_SESSION_BUS_ADDRESS',
           'DEFAULTS_PATH',
           'DESKTOP_SESSION',
           'DISPLAY',
           'GDMSESSION',
           'GDM_KEYBOARD_LAYOUT',
           'GDM_LANG',
           'GNOME_DESKTOP_SESSION_ID',
           'GNOME_KEYRING_CONTROL',
           'GNOME_KEYRING_PID',
           'GTK_MODULES',
           'HOME',
           'LANG',
           'LOGNAME',
           'LOGNAME',
           'MAIL',
           'MANDATORY_PATH',
           'ORBIT_SOCKETDIR',
           'SESSION_MANAGER',
           'SHELL',
           'SSH_AGENT_PID',
           'SSH_AUTH_SOCK',
           'SSH_CLIENT',
           'SSH_CONNECTION',
           'SSH_TTY',
           'TERM',
           'USER',
           'USERNAME',
           'WINDOWID',
           'XAUTHORITY',
           'XDG_CONFIG_DIRS',
           'XDG_DATA_DIRS',
           'XDG_SESSION_COOKIE',
           '_',
           envs_path_var,
           env_var,
           configs_path_var,
           configs_loaded_var]


def usage(args):
    """prints albion usage information

    output of this should *not* be evaled

    """
    print >> sys.stderr, 'Usage:'
    print >> sys.stderr, ''
    print >> sys.stderr, '  albion command'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Command is one of:'
    print >> sys.stderr, ''
    print >> sys.stderr, '  help          display this information'
    print >> sys.stderr, '  list-envs     list all available environments'
    print >> sys.stderr, '  list-configs  list all available configurations'
    print >> sys.stderr, '  load          load a configuration into your ' \
    'environment; with no args, list loaded configurations'
    print >> sys.stderr, '  unload        unload a configuration from your' \
    ' environment'
    print >> sys.stderr, '  env           set up an environment; with no' \
        ' args, list current environment'
    print >> sys.stderr, ''


def check_path(path_var):
    if path_var not in os.environ:
        print path_var + ' is not set'
        sys.exit(-1)


def load(args):
    """loads a configuration

    the output of this should be evaled

    """
    # REVISIT: should we check if config is already loaded and if so,
    # don't load it, even if version is different (assume it's a
    # conflict)?
    if len(args) < 1:
        for config in os.environ[configs_loaded_var].split(':'):
            if config:
                fields = config.split('+')
                print >> sys.stderr, '%s %s' % (fields[0], fields[1])
        sys.exit(0)
    if len(args) < 2:
        print >> sys.stderr, 'albion: not enough arguments to load'
        sys.exit(-1)
    config = args[0]
    version = args[1]
    check_path(configs_path_var)
    found_config = False
    found_config_version = False
    configs_full_path = ''
    for configdir in os.environ[configs_path_var].split(':'):
        if not os.path.exists(configdir + '/' + config):
            continue
        # we found a config directory for requested config
        found_config = True
        config_full_path = configdir + '/' + config + '/' + version
        if not os.path.isfile(config_full_path):
            # we didn't find the specified version of the config in
            # this config directory
            continue
        found_config_version = True
        break
    if not found_config:
        print >> sys.stderr, 'albion: config %s not found' % config
        sys.exit(-1)
    if not found_config_version:
        print >> sys.stderr, 'albion: configs for %s found, but version ' \
            '%s not found' % (config, version)
        sys.exit(-1)
    print '. %s;' % config_full_path
    print 'export %s="$%s:%s+%s";' % (
        configs_loaded_var, configs_loaded_var, config, version)


def find_env(env):
    check_path(envs_path_var)
    found_env = False
    env_full_path = ''
    for envdir in os.environ[envs_path_var].split(':'):
        if not os.path.exists(envdir + '/' + env):
            continue
        found_env = True
        env_full_path = envdir + '/' + env
        break
    if not found_env:
        print >> sys.stderr, 'albion: env %s not found' % env
        sys.exit(-1)
    return env_full_path


def env_load(args):
    """Finds an environment to load.

    output of this should be evaled

    this should not be called directly by a user

    """
    assert(len(args) == 1)
    env_full_path = find_env(args[0])
    print '. %s;' % env_full_path


def env(args):
    """Loads an environment (which usually loads some configs)

    output of this should be evaled

    """
    if len(args) < 1:
        print >> sys.stderr, os.environ[env_var]
        sys.exit(0)
    if len(args) > 1:
        print >> sys.stderr, 'albion: too many arguments, did you mean load?'
        sys.exit(-1)
    env = args[0]
    find_env(env)
    print 'export %s="%s";' % (env_var, env)
    purgeenv()


def unload(args):
    """unloads a configuration

    output of this should be evaled

    """
    if len(args) < 1:
        print >> sys.stderr, 'albion: not enough arguments to unload'
        sys.exit(-1)
    config_to_unload = args[0]
    check_path(configs_loaded_var)
    loaded_configs = ''
    for loaded_config in os.environ[configs_loaded_var].split(':'):
        if config_to_unload in loaded_config:
            continue
        loaded_configs += loaded_config + ':'
    print 'export %s=%s' % (configs_loaded_var, loaded_configs)
    purgeenv()


def list(paths_var, things):
    """lists available environments or configs

    things is the thing you are listing, plural

    output of this should *not* be evaled

    """
    check_path(paths_var)
    print >> sys.stderr, ''
    for path in os.environ[paths_var].split(':'):
        print >> sys.stderr, '%s in %s:' % (things, path)
        print >> sys.stderr, ''
        for item in os.listdir(path):
            print >> sys.stderr, '  ' + item
        print >> sys.stderr, ''


def list_envs(args):
    list(envs_path_var, 'environments')


def list_configs(args):
    list(configs_path_var, 'configurations')


def which(args):
    """report where a given named item comes from

    the output of this should *not* be evaled

    """
    if len(args) < 1:
        print >> sys.stderr, 'albion: not enough arguments to which'
        sys.exit(-1)

    # it could be a configuration, so search those:
    check_path(configs_path_var)
    for configdir in os.environ[configs_path_var].split(':'):
        if not os.path.exists(configdir + '/' + args[0]):
            continue
        # found a config by that name:
        print >> sys.stderr, 'configuration:'
        print >> sys.stderr, '  ' + configdir + '/' + args[0]

    # it could be an environment, so search those:
    check_path(envs_path_var)
    for envdir in os.environ[envs_path_var].split(':'):
        if not os.path.exists(envdir + '/' + args[0]):
            continue
        # found an env by that name:
        print >> sys.stderr, 'environment:'
        print >> sys.stderr, '  ' + envdir + '/' + args[0]


def purgeenv():
    """purges all environment variables prior to loading an environment

    the output of this should be evaled

    """
    for key in os.environ:
        if key not in keepers:
            print 'unset ' + key + ';'
    print 'exec ' + os.environ['SHELL'] + ' -l;'

commands = {'env': env,
            'environment': env,
            'env_load': env_load,
            'help': usage,
            'list-envs': list_envs,
            'list-configs': list_configs,
            'lo': load,
            'loa': load,
            'load': load,
            'un': unload,
            'unl': unload,
            'unlo': unload,
            'unloa': unload,
            'unload': unload,
            'which': which}


def main():
    if len(sys.argv) < 2:
        usage(0)
        sys.exit(0)
    if sys.argv[1] in commands:
        commands[sys.argv[1]](sys.argv[2:])
    else:
        print >> sys.stderr, 'albion: there is no "%s" command' % sys.argv[1]
        sys.exit(-1)

if __name__ == "__main__":
    main()
