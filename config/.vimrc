nnoremap <silent> <SPACE> :nohlsearch<CR>

syntax on
filetype indent plugin on

set scrolloff=3
set number
set autoindent
set tags=./tags,tags;

autocmd BufRead,BufNewFile *.pc set filetype=c

autocmd FileType python setlocal tabstop=4 expandtab shiftwidth=4 softtabstop=4
"autocmd FileType python setlocal tabstop=4 noexpandtab shiftwidth=4 softtabstop=4
