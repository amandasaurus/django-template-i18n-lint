" Enter :make to get a list of the messages
set makeprg=django-template-i18n-lint.py
set errorformat=%f:%l:%c:%m

" Press <F8> to easily get to the next un-translated string
map <F8> :cnext<enter>

" select some text in visual mode, then call the e macro on it (e.g. press
" @e), and it'll wrap that text in {% blocktrans %}/{% endblocktrans %}
let @e = "`>a{% endblocktrans %}gv`<i{% blocktrans %}"

" select some text in visual mode, then call the w macro on it (e.g. press
" @w), and it'll wrap that text in {% trans "" %}
let @w = '`>a" %}gv`<i{% trans "l'
