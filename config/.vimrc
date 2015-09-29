nnoremap <silent> <SPACE> :nohlsearch<CR>

syntax on
filetype indent plugin on

set number
set autoindent
set tags=./tags,tags;

autocmd BufRead,BufNewFile *.pc set filetype=c

autocmd FileType python setlocal tabstop=8 expandtab shiftwidth=4 softtabstop=4
