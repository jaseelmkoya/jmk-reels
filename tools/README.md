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

## Reach rules (JMK, 13 Nov — from the first 3 days of stats)
Facts: JMK's own face/experiment reels got ~3x the views of our text animations (Torque 3,876 vs 387–1,366).
Meteor (trending hook + JMK's own thumbnail + voice) did best of ours: 1,366 IG views, 44 shares, 1,066 YT.
1. LENGTH: default 30–40 s for animated reels (end-card not counted), one idea per reel, cut filler.
   JMK (13 Nov): if the subject is genuinely interesting and needs more time, there is NO time limit — keep it tight, but don't cut good content just to hit 40 s.
2. FIRST SECOND = HOOK: frame 0 already shows the big question/claim + a moving visual (no slow fade-in, no tag pill first;
   the "PLUS ONE PHYSICS" tag comes in small after ~1.5 s). The hook question must make people curious ("…safe ആണോ?").
3. CAPTION: first line = the hook question (with 1 emoji), then 2–3 short lines, the quiz, "Follow ചെയ്യൂ 🔔";
   only 5–6 relevant hashtags (no long hashtag walls).
4. FACE HOOK (optional): if JMK sends a 3–8 s phone clip of himself asking the hook, put it first with
   `python3 prepend_hook.py <clip> <reel.mp4> <out.mp4>` (before endcard.py), and shorten the animated part accordingly.

## Weekly "avatar explainer" format (JMK, 13 Nov — experiment, once a week)
Maroon theme, JMK's cartoon avatar bottom-right that talks with the voice (tools/avatar.py + brand/avatar_{closed,talk,blink}.png,
made once from his photo; no credits per video). Example: tools/topics/avatar_demo.py (bus-brake demo).
Needs a voice (AI voice on request, or his recording). Hook text visible from frame 0, centre animation, "BREAKING"-style chip,
word-by-word captions, end-cards as usual.

## News-first topic research (JMK, 14 Nov — missed the Kolkata–Sairang Express derailment, Assam, 11 Nov)
Before picking ANY topic, scan real news of the last 48–72 h (India + Kerala), not only "science news":
run at least 6 separate WebSearches, e.g. "<today> India news", "Kerala news today", "accident India this week" (train, bus,
plane, boat, fire), "weather Kerala today" (rain, lightning, heat, cyclone), "ISRO / space news this week", "viral video India
this week", "sports India this week", "technology launch India this week". Make a shortlist of 5–8 stories and ask:
which one connects naturally to Plus One / Plus Two physics (momentum, inertia, braking, friction, pressure, waves,
electricity, optics, gravitation, heat …)? A big news story with a clear physics link beats any syllabus topic.
Accidents / disasters: respectful tone, no gore, no blame, verified facts only (name the source), focus on the physics
and on safety; if people died, avoid jokes/dramatic music and mention it gently or pick a different angle.
Write the shortlist (with links) into STATUS.md so JMK can see what was considered.
