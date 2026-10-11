#!/bin/bash
# Build the themes of the ports into OUTDIR from the vakio palette
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 OUTDIR" >&2
    exit 1
fi
outdir=$1
portsdir=$(dirname "$0")
mkdir -p "$outdir"

macros=$(mktemp)
trap 'rm -f "$macros"' EXIT
{
    # The colours start with #, which would start an m4 comment
    echo 'm4_changecom()m4_dnl'
    vakio --keys semantic --keys ansi --keys rainbow --to m4
    vakio --keys catppuccin --to m4 --m4prefix latte_
} >"$macros"

build() {
    m4 -P "$macros" "$portsdir/../m4/translate_seq.m4" "$portsdir/$1" \
        >"$outdir/$2"
}
build kitty.conf.m4 vakio.conf
build micro.m4 vakio.micro
build fish.theme.m4 vakio.theme
build fzf.fish.m4 vakio_fzf_colors.fish
build bat.tmTheme.m4 vakio.tmTheme
