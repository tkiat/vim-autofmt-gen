#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
import argparse
import glob
import os
import sys
import yaml

parser = argparse.ArgumentParser(
    description='Generate autoformatter plugins for vim and neovim')
parser.add_argument(
    "-c",
    "--config",
    type=str,
    default='~/.config/vim-autofmt-gen/config.yaml',
    metavar="STR",
    help="config path (default: %(default)s)",
)
parser.add_argument("-d",
                    "--delete",
                    action="store_true",
                    help="delete all generated plugins")

args = parser.parse_args()
CONFIG_PATH = os.path.expanduser(args.config)
DELETE_GENERATED_THEN_EXIT = args.delete

if DELETE_GENERATED_THEN_EXIT:
    with open(CONFIG_PATH, 'r') as f:
        ftplugin_dir = ""
        try:
            list = yaml.load(f, Loader=yaml.FullLoader)
            configs = list.items()
            for key, value in configs:
                if key == 'settings':
                    settings = value
                    ftplugin_dir = os.path.expanduser(settings['folder-dir'])
                    break
            for f in glob.iglob(ftplugin_dir + "/**/autofmtgen_*",
                                recursive=True):
                print('Deleting ' + f + ' ...')
                os.remove(f)
        except yaml.YAMLError as err:
            print(err)
    sys.exit()

with open(CONFIG_PATH, 'r') as f:
    mapping = {}
    ftplugin_dir = ""
    script_path = ""
    try:
        list = yaml.load(f, Loader=yaml.FullLoader)
        configs = list.items()
        for key, value in configs:
            if key == 'settings':
                settings = value
                ftplugin_dir = os.path.expanduser(settings['folder-dir'])
                script_path = os.path.expanduser(settings['script-path'])
                os.makedirs(ftplugin_dir, 0o755, exist_ok=True)
            elif key == 'plugins':
                env = Environment(loader=FileSystemLoader('templates'))
                template = env.get_template('plugin.vim')
                #
                ftplugins = value.items()
                for ftplugin in ftplugins:
                    (ft, plugins) = ftplugin
                    mapping[ft] = []
                    ft_dir = ftplugin_dir + '/' + ft
                    os.makedirs(ft_dir, 0o755, exist_ok=True)
                    for plugin in plugins:
                        cmd = plugin['cmd']
                        arg = '' if plugin['arg'] is None else plugin['arg']
                        if cmd != None:
                            output = template.render(cmd=cmd, arg=arg, ft=ft)
                            plugin_dir = ft_dir + '/autofmtgen_' + str.lower(
                                cmd) + '.vim'
                            print('Creating ' + plugin_dir + ' ...')
                            with open(plugin_dir, "w") as f:
                                f.write(output)
                            mapping[ft].append(cmd)
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('script.vim')
        output = template.render(_dict=mapping)

        print('Creating ' + script_path + ' ...')
        os.makedirs(os.path.dirname(script_path), 0o755, exist_ok=True)
        with open(script_path, "w") as f:
            f.write(output)
    except yaml.YAMLError as err:
        print(err)
