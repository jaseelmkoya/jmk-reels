#!/bin/bash
# name src start end cropfilter
ex(){ mkdir -p frames/$1; rm -f frames/$1/*.jpg; ffmpeg -v error -y -ss $3 -to $4 -i src/$2.mp4 -vf "fps=30,$5,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6" -q:v 3 frames/$1/%04d.jpg; echo "$1 $(ls frames/$1 | wc -l)"; }
A="crop=506:900:905:0"           # 2316x1080 screen recordings (HUD cut off)
B="crop=415:738:753:0"           # 1920x886 recording (catch)
ex catch_desc c2 10.6 25.0 $B &
ex catch_close c2 25.0 30.5 $B &
ex catch_hold c2 30.5 40.0 $B &
ex lift_close c1 2.9 10.0 $A &
wait
ex lift_aerial c1 10.2 19.0 $A &
ex lift_sky c1 19.2 29.8 $A &
ex starlink c3 4.2 8.3 $A &
ex earth_flap c4 41.0 47.5 $A &
wait
ex plasma_a c4 11.5 36.0 $A &
ex plasma_b c4 52.0 88.0 $A &
ex belly c5 0.0 3.3 $A &
wait
