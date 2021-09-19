" Generated by vim-autofmt-gen
let s:command = "{{ cmd }}"
let s:arguments = "{{ arg }}"

if exists("g:autofmtgen_{{ ft }}_{{ cmd|lower }}_skip") && g:autofmtgen_{{ ft }}_{{ cmd|lower }}_skip == 1
  finish
endif
let g:autofmtgen_{{ ft }}_{{ cmd|lower }}_skip = 1

augroup {{ cmd|lower }}
  autocmd!
  autocmd BufWritePre <buffer> call autofmtgen_{{ cmd|lower }}#TryToApply()
augroup END
" ==============================================================================
" Commands
" ==============================================================================
command! {{ cmd|capitalize }}Continue exe "call autofmtgen_{{ cmd|lower }}#Continue()"
command! {{ cmd|capitalize }}Pause    exe "call autofmtgen_{{ cmd|lower }}#Pause()"

function! autofmtgen_{{ cmd|lower }}#Continue()
  let g:{{ ft }}_{{ cmd|lower }}_pause = 0
endfunction

function! autofmtgen_{{ cmd|lower }}#Pause()
  let g:{{ ft }}_{{ cmd|lower }}_pause = 1
endfunction
" ==============================================================================
" Helping Functions
" ==============================================================================
function! autofmtgen_{{ cmd|lower }}#Apply() range
  silent! exe "keepjumps " . a:firstline . "," . a:lastline . "!" . s:command . " " . s:arguments
  call winrestview(b:winview)
endfunction

function! autofmtgen_{{ cmd|lower }}#ShouldApply()
  if exists("g:{{ ft }}_{{ cmd|lower }}_pause") && g:{{ ft }}_{{ cmd|lower }}_pause == 1
    return 0
  endif

  if !executable(s:command)
    echoerr "autofmtgen_{{ cmd|lower }}.vim: " . s:command . " not found in $PATH"
    return 0
  endif

  silent! exe "w !" . s:command . s:arguments . " > /dev/null 2>&1"
  if v:shell_error
    echoerr "autofmtgen_{{ cmd|lower }}.vim: " . s:command . s:arguments . " is not valid"
    return 0
  endif

  return 1
endfunction

function! autofmtgen_{{ cmd|lower }}#TryToApply()
  if autofmtgen_{{ cmd|lower }}#ShouldApply()
    let b:winview = winsaveview()
    exe "%call autofmtgen_{{ cmd|lower }}#Apply()"
  endif
endfunction