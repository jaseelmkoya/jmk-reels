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
never per letter (conjuncts would break). For voiced videos ALWAYS get exact word times: ElevenLabs creative_transcribe_audio (eleven_scribe_v1, 0 credits) on the speech node → words[].start → Captions.from_words(lines, words). Display tokens must match spoken words 1:1. See topics/story_raman_vo.py + story_raman_words.json.

## Platform end-cards (endcard.py) — JMK, 12 Nov
Every reel gets two exports with a 4 s end animation appended:
`python3 endcard.py <final.mp4> <prefix>` → `<prefix>_ig.mp4` (blue "Follow" tapped → "Following", hearts)
and `<prefix>_yt.mp4` (red "SUBSCRIBE" tapped → "SUBSCRIBED", then bell tapped and ringing).
Instagram ALWAYS gets the _ig file, YouTube ALWAYS gets the _yt file → publish them as two separate Uplika posts.
Only the apps' button styles are imitated; the Instagram/YouTube logos are never drawn.
