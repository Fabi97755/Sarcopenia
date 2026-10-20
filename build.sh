#!/usr/bin/env bash
# Crea la versione standalone (con doctype) da sarcopenia.html e registra l'MP4.
set -e
cd "$(dirname "$0")"
{ echo '<!doctype html><html><head><meta charset="utf-8"><title>Sarcopenia</title></head><body>'; grep -v '^<title>' sarcopenia.html; echo '</body></html>'; } > sarcopenia_standalone.html
node record.js sarcopenia_standalone.html sarcopenia.mp4
