# vim-autofmt-gen

A single-script Vim/Neovim autoformatter plugin generator for CLI-based autoformatters (like yapf, brittany, js-beautify) based on Jinja 2 templating engine and Python3.

I did this because I saw the same pattern in many Vim/Neovim autoformatter plugins so I decided to write the Jinja template once. More advanced solutions probably exists but this is simple enough and fits my need. All it does are checking if the command and arguments are valid before automatically applying it upon saving the file and providing the user the option to pause/resume the autoformatter as well.

## Installation

1. Execute the script directly

    Install `Jinja2` and `PyYAML` and then execute the script (vim-autofmt-gen.py) directly
1. Nix
    ```bash
    $ git clone https://github.com/tkiat/vim-autofmt-gen.git && cd vim-autofmt-gen
    $ nix-build --attr exe && nix-env -i ./result
    ```
1. Nix Flakes (Experimental)
    ```bash
    $ nix build github:tkiat/vim-autofmt-gen --out-link vim-autofmt-gen && nix-env -i ./vim-autofmt-gen
    ```

## Usage

First, create a YAML config file like this.

```yaml
- ftplugin-dir: ~/.config/nvim/ftplugin
- plugins:
  - javascript:
    - cmd: js-beautify
      arg:
  - python:
    - cmd: yapf
      arg:
  - haskell:
    - cmd: brittany
      arg: --columns 80 --indent 2
    - cmd: hindent
      arg: --indent-size 2 --line-length 80
```

- `ftplugin-dir` is the the ftplugin folder (typically `~/.vim/ftplugin` for Vim and `~/.config/nvim/ftplugin` for Neovim). The generator will create all plugins in this folder.
- Each entry in the `plugins` field is a filetype recognized by Vim. To view possible filetypes, enter `:setfiletype` then space then CTRL+D in Vim/Neovim. Only the first autoformatter of the filetype will be applied, in this case, only brittany will be applied, not hindent.

To create autoformatter plugins,

```bash
$ ./vim-autofmt-gen.py -p <path-to-your-config> -c
```

To remove generated autoformatter plugins,

```bash
$ ./vim-autofmt-gen.py -p <path-to-your-config> -r
```

## Commands in Vim/Neovim

Say you generated a `brittany` Haskell autoformatter plugin. After opening a Haskell file,

- `:BrittanyPause` will pause the autoformatter plugin
- `:BrittanyContinue` will continue the autoformatter plugin
- It will output a warning if it cannot apply the `brittany <your-argments>` command successfully. This can happen when `brittany` is not found in $PATH.
- On save, it will test the autoformatter once and will not actually format in the case of an error
