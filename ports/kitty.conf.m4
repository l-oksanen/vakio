m4_divert(-1)
# Built into vakio.conf by ports/build.sh.
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
