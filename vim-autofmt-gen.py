#!/usr/bin/env python3
import argparse
import glob
from jinja2 import Environment, BaseLoader
import os
from pathlib import Path
import yaml

TEMPLATE = """" Generated by vim-autofmt-gen
" This can be overwritten by the next invocation of it
let s:command = "{{ cmd }}"
let s:arguments = "{{ arg }}"

if exists("g:autofmtgen_{{ ft }}_{{ cmd|replace("-", "_")|lower }}_skip") && g:autofmtgen_{{ ft }}_{{ cmd|replace("-", "_")|lower }}_skip == 1
  finish
endif
let g:autofmtgen_{{ ft }}_{{ cmd|replace("-", "_")|lower }}_skip = 1

augroup {{ cmd|replace("-", "_")|lower }}
  autocmd!
  autocmd BufWritePre <buffer> call autofmtgen_{{ cmd|replace("-", "_")|lower }}#TryToApply()
  autocmd FileType {{ ft }}
    \ autocmd BufWritePre <buffer> call autofmtgen_{{ cmd|replace("-", "_")|lower }}#TryToApply()
augroup END
" ==============================================================================
" Commands
" ==============================================================================
command! {{ cmd|replace("-", "")|capitalize }}Continue exe "call autofmtgen_{{ cmd|replace("-", "_")|lower }}#Continue()"
command! {{ cmd|replace("-", "")|capitalize }}Pause    exe "call autofmtgen_{{ cmd|replace("-", "_")|lower }}#Pause()"

function! autofmtgen_{{ cmd|replace("-", "_")|lower }}#Continue()
  let g:{{ ft }}_{{ cmd|replace("-", "_")|lower }}_pause = 0
endfunction

function! autofmtgen_{{ cmd|replace("-", "_")|lower }}#Pause()
  let g:{{ ft }}_{{ cmd|replace("-", "_")|lower }}_pause = 1
endfunction
" ==============================================================================
" Helping Functions
" ==============================================================================
function! autofmtgen_{{ cmd|replace("-", "_")|lower }}#Apply() range
  silent! exe "keepjumps " . a:firstline . "," . a:lastline . "!" . s:command . " " . s:arguments
  call winrestview(b:winview)
endfunction

function! autofmtgen_{{ cmd|replace("-", "_")|lower }}#ShouldApply()
  if exists("g:{{ ft }}_{{ cmd|replace("-", "_")|lower }}_pause") && g:{{ ft }}_{{ cmd|replace("-", "_")|lower }}_pause == 1
    return 0
  endif

  if !executable(s:command)
    echoerr "autofmtgen_{{ cmd|replace("-", "_")|lower }}.vim: " . s:command . " not found in $PATH"
    return 0
  endif

  silent! exe "w !" . s:command . " " . s:arguments . " > /dev/null 2>&1"
  if v:shell_error
    echoerr "autofmtgen_{{ cmd|replace("-", "_")|lower }}.vim: " . s:command . " " . s:arguments . " is not valid"
    return 0
  endif

  return 1
endfunction

function! autofmtgen_{{ cmd|replace("-", "_")|lower }}#TryToApply()
  if autofmtgen_{{ cmd|replace("-", "_")|lower }}#ShouldApply()
    let b:winview = winsaveview()
    exe "%call autofmtgen_{{ cmd|replace("-", "_")|lower }}#Apply()"
  endif
endfunction
"""

# -----------------------------------------------------------------------------


def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description='Generate autoformatter plugins for Vim and Neovim')
    p.add_argument(
        "-p",
        "--path",
        type=str,
        metavar="STR",
        help="path of your YAML config file",
        required=True,
        #         default=XDG_CONFIG_HOME + '/vim-autofmt-gen/config.yaml',
        #         help="config path (default: %(default)s)",
    )

    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("-c",
                   "--create",
                   action="store_true",
                   help="created autoformatter plugins")
    g.add_argument("-r",
                   "--remove",
                   action="store_true",
                   help="remove all generated autoformatter plugins")
    return p


# -----------------------------------------------------------------------------
parser = create_parser()
args = parser.parse_args()

CONFIG_PATH = os.path.expanduser(args.path)

with open(CONFIG_PATH, 'r') as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)
    dest_dir = os.path.expanduser(configs['ftplugin-dir'])
    ftplugins = configs['plugins']
    if args.remove:
        try:
            for f in glob.iglob(dest_dir + "/**/autofmtgen_*", recursive=True):
                print('Removing ' + f + ' ...')
                os.remove(f)
        except yaml.YAMLError as err:
            print(err)
    elif args.create:
        template = Environment(loader=BaseLoader()).from_string(TEMPLATE)
        try:
            os.makedirs(dest_dir, 0o755, exist_ok=True)
            for ftplugin in ftplugins:
                (ft, plugins) = list(ftplugin.items())[0]
                ft_dir = dest_dir + '/' + ft
                os.makedirs(ft_dir, 0o755, exist_ok=True)
                plugin = plugins[0]  # apply only first autoformatter
                cmd = plugin['cmd']
                arg = '' if plugin['arg'] is None else plugin['arg']
                if cmd != None:
                    output = template.render(cmd=cmd, arg=arg, ft=ft)
                    plugin_path = ft_dir + '/autofmtgen_' + str.lower(
                        cmd).replace('-', '_') + '.vim'
                    action_text = 'Updating ' if Path(
                        plugin_path).is_file() else 'Creating '
                    print(action_text + plugin_path + ' ...')
                    with open(plugin_path, "w") as f:
                        f.write(output)
        except yaml.YAMLError as err:
            print(err)
