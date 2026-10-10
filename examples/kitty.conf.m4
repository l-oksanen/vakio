m4_divert(-1)
# The default palette can be injected into this template by using 
# the following command in fish shell: 
#
# m4 -P (vakio | psub) m4/translate_seq.m4 examples/kitty.conf.m4
#
# The process substitution (vakio | psub) must be adjusted for other
# shells. Alternatively, redirect first to a file 
#
# vakio > colormap.m4
#
# and use colormap.m4 in place of the process substitution.
#
# For instructions on how to use the theme in kitty, see 
#
# https://sw.kovidgoyal.net/kitty/kittens/themes/
#
m4_divert(0)m4_dnl

foreground vakio_text
background vakio_base
# selection_foreground TODO
# selection_background TODO

url_color vakio_operators

active_tab_foreground vakio_labels
active_tab_background vakio_base
inactive_tab_foreground vakio_subtle
inactive_tab_background vakio_mantle
tab_bar_background vakio_mantle
tab_bar_margin_color vakio_mantle

vakio_translate_seq(vakio_ansi, color, 0, 16, 
vakio_key vakio_value
)
