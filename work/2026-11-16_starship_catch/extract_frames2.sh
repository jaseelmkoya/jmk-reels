#!/bin/bash
ex(){ mkdir -p frames/$1; rm -f frames/$1/*.jpg; ffmpeg -v error -y -ss $3 -to $4 -i src/$2.mp4 -vf "fps=30,$5,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6" -q:v 3 frames/$1/%04d.jpg; echo "$1 $(ls frames/$1 | wc -l)"; }
C="crop=423:752:734:0"           # 1920x896 recordings (HUD cut off)
ex plasma_c c6 0.0 27.6 $C &
ex boost_burn c7 13.6 27.0 $C &
ex boost_boom c7 40.8 43.6 $C &
wait
# boost_boom: ffmpeg -ss 40.8 -to 43.6 -i src/c7.mp4 -filter_complex "fps=30,crop=766:452:700:300,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24,eq=brightness=-0.18[bg];[b]scale=1080:-2,unsharp=5:5:0.6[fg];[bg][fg]overlay=0:(H-h)/2-60" frames/boost_boom/%04d.jpg
