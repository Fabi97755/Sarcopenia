#!/usr/bin/env bash
# Crea la versione standalone (con doctype) da sarcopenia.html e registra l'MP4.
set -e
cd "$(dirname "$0")"
{ echo '<!doctype html><html><head><meta charset="utf-8"><title>Sarcopenia</title></head><body>'; grep -v '^<title>' sarcopenia.html; echo '</body></html>'; } > sarcopenia_standalone.html
node record.js sarcopenia_standalone.html sarcopenia.mp4
# Versione per PowerPoint (H.264 Main 4.0, keyframe ogni 2 s) e immagine di anteprima (titolo a t = 2 s).
ffmpeg -loglevel error -y -i sarcopenia.mp4 -c:v libx264 -profile:v main -level 4.0 -pix_fmt yuv420p -crf 24 -preset slow -maxrate 3M -bufsize 6M -g 60 -an -movflags +faststart sarcopenia_powerpoint.mp4
ffmpeg -loglevel error -y -ss 2 -i sarcopenia.mp4 -frames:v 1 sarcopenia_anteprima.png
