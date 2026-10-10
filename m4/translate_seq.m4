m4_divert(-1)

m4_define(`vakio_translate_seq_loop', 
  `
  m4_ifelse(m4_eval($3 < $4), 1, 
    `
    m4_define(`vakio_key', ``$2$3'')
    m4_define(`vakio_value', `$1$3')
    m4_divert(0)$5m4_divert(-1)
    vakio_translate_seq_loop(`$1', `$2', m4_incr($3), $4, `$5')
    '
  )
  '
)

m4_define(`vakio_translate_seq', 
  `m4_divert(-1)
  vakio_translate_seq_loop(`$1', `$2', $3, $4, `$5')
  m4_divert(0)m4_dnl'
)

m4_divert(0)m4_dnl
