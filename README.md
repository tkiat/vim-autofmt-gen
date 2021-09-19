# vim-autofmt-gen

An autoformatter plugins generator for Vim and Neovim. Just put any autoformatter commands and their arguments in a Yaml file and you are set.

## Why?

There are many autoformatter plugins already but they usually have determined list of supported plugins and their configs. With this generator, you can insert any autoformatter and the corresponding arguments (e.g. column width) however you like.

## Installation

### Using nix

```
nix-build --attr exe
```

### Without nix

Install jinja2 and pyyaml then run the script (vim-autofmt-gen.py) directly.

## Usage

### Example config file

```yaml
settings:
  folder-dir: ~/.config/nvim/ftplugin
  script-path: ~/.config/nvim/vim/autofmtgen.vim

plugins:
  python:
    - cmd: yapf
      arg:
  haskell:
    - cmd: brittany
      arg: --columns 80 --indent 2
    - cmd: hindent
      arg: --indent-size 2 --line-length 80
```

- `folder-dir` is the folder where all generated plugins will live which should be a `ftplugin` folder. It is usually at ~/.vim/ftplugin for Vim.
- `script-path` is the script with flags to enable each generated plugin on start. You can source this file in your (n)vim config.
- Each entry in the `plugins` field is a filetype recognized by Vim. Enter :setfiletype then space then CTRL+D to view possible filetypes
- In the case of more than two plugins for one filetype, only the topmost one will be enabled by default, in this case `yapf` and `brittany`

### Commands

Simply add a config file at ~/.config/vim-autofmt-gen/config.yaml then type

```
vim-autofmt-gen
echo "or run script directly"
./vim-autofmt-gen.py
```

This will generate all plugins. To delete those later, type

```
vim-autofmt-gen --delete
echo "or run script directly"
./vim-autofmt-gen.py --delete
```

### Usage in Vim/Neovim

Say you have generated a Brittany plugin and also enabled it on start. After opening a Haskell file,

- `BrittanyPause` will pause the plugin
- `BrittanyContinue` will continue
- It will output a warning if `brittany` is not found in $PATH.
- It will mock the formatter once and will not actually format in the case of an error.
