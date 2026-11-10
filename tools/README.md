# Reel tools (approved 10 Nov 2026)
- reelkit.py — renderer (watermark at bottom, WM_Y=1620). Needs fonts/NotoSansMalayalam-{Regular,Bold}.ttf next to it.
- make_cover.py — cover image.
- mix_voice.py — `python3 mix_voice.py topics/<slug>.py out/<silent>.mp4 out/<final>.mp4`; topic defines VOICE (48 kHz wav path, relative to tools/) and SFX list.
- topics/inertia_vo.py — example synced to a real voice-over (scene lengths & text times = speech times).

## Background music (music.py)
Music changes with the scene and the video. In a topic file set
`MUSIC = [(start_s, "mood"), ...]` — moods: space, cinematic, ocean, curious, tension, uplift, electric.
Pick moods by what the scene is doing (story opening → cinematic, space → space, explaining → curious,
quiz / "why?" → tension, discovery / ending → uplift, electricity/magnetism → electric).
The key changes per video (seed from the topic name), so no two videos sound the same.

## Word-by-word captions (captions.py)
Narration text appears word by word, in time with the voice (word times spread over the real speech
found by silencedetect). Without voice, words appear at reading pace. Malayalam is revealed per word,
never per letter (conjuncts would break). See topics/story_raman_vo.py (CAP = Captions(...); CAP.draw(fr, time, y)).
