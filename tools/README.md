# Reel tools (approved 10 Nov 2026)
- reelkit.py — renderer (watermark at bottom, WM_Y=1620). Needs fonts/NotoSansMalayalam-{Regular,Bold}.ttf next to it.
- make_cover.py — cover image.
- mix_voice.py — `python3 mix_voice.py topics/<slug>.py out/<silent>.mp4 out/<final>.mp4`; topic defines VOICE (48 kHz wav path, relative to tools/) and SFX list.
- topics/inertia_vo.py — example synced to a real voice-over (scene lengths & text times = speech times).
