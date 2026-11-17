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
- JMK 15 Nov: "light music" too soft → new moods hype / drive (lead hook + real drums) and MUSIC_GAIN in the topic (0.45 = louder bed). No small English mono strips/pins on screen unless asked.

## Tracker sheet (JMK, 15 Nov)
Every reel made in any chat goes into JMK's Claude Sheet "JMK Reels Tracker": https://claude.ai/artifact/Qqi5yndGdihmdjz5tTHWc1
(Claude Docs project c10f35cf-2661-4d6c-867d-e7cc5363cb82, workbook node 16b1792c-c9bf, sheet "Reels", header row 5, columns A–N:
# | തീയതി | Video | Claude-ൽ? | Status | IG views | YT views | Instagram post | YouTube post | Class · Chapter | Voice | Instagram link | YouTube link | കുറിപ്പ്).
When you make, schedule, post, hold or change a reel: add or update its row (date order; no duplicates; never delete rows or change JMK's "Claude-ൽ?" choices).
Use the Claude Docs connector (guide topic.sheets first; read before every write). The 7:37 daily task also refreshes views for the last 7 days.


## Thumbnail / cover style (JMK, 16 Nov 2026 — "ഈ രീതി വേണം തമ്പ്നെയിലുണ്ടാക്കാൻ")
Reference: work/2026-11-16_starship_catch/starship_catch_thumb_jmk.jpg (JMK's own). Tool: `python3 make_thumb.py BG.jpg OUT.jpg --top "<Malayalam claim>" --en "<ENGLISH PUNCH!>" --mid "<line1>|<line2>|<line3>" [--focus 0.35] [--side right]`
- One dramatic, SHARP, high-resolution photo of the subject filling the 9:16 frame (subject on the left/centre). Prefer a clean still (official photo, Google Flow / AI still) over a blurry webcast frame; the tool grades it (contrast, teal-orange, vignette, red edge glow, sparks).
- Top: huge Malayalam claim in yellow (#FFE814), heavy Anek Malayalam ExtraBold, thick dark outline + red outer glow, ONE line if possible ("ചരിത്രം കുറിച്ച്").
- Under it on the right: one big white condensed English punch word (Bebas Neue): "SPACE X!".
- Middle right, beside the subject: 2–3 short yellow Malayalam lines saying what happened ("റോക്കറ്റിനെ | കൈകൊണ്ട് | പിടിച്ച് ടവർ!").
- Bottom right: JMK's shocked reaction cut-out, big (brand/faces/jmk_shock.png; add more expressions to brand/faces/ when JMK sends photos).
- Few words, no small text, no logos. Instagram reel cover = this image (coverMediaId). YouTube Shorts take no custom thumbnail through the API.

## Quiz = PYQ check, every reel (JMK, 17 Nov 2026 — "ഇനി ഇങ്ങനെ ആവർത്തിക്കരുത്, കൃത്യമായി നോക്കണം")
The 17 Nov aeroplane reel went out to JMK with "concept quiz, no PYQ label" although the question was Plus One Model Exam 2020.
Before writing ANY quiz: load the PYQ skill for the class (plus-one-physics-pyq / plus-two PYQ skill) and search the chapter's bank for the
quiz question. If it is there, show the exact label on screen (pill "PYQ · Plus One Model Exam 2020"), in both captions and in the voice-over script.
Write "concept quiz, no PYQ label" only after the bank was actually searched and the question is not in it — and say so in STATUS.md.
