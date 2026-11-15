# 2026-11-16 · SpaceX Starship Flight 15 — Ship 42 caught by the launch tower (made 15 Nov night in JMK's chat)
Status: SCHEDULED 16 Nov 18:30 IST (no voice) — Instagram post_b7ac3c056c7a50f9 (cover med_cff3a495bfdd973f), YouTube post_46e08d83e2d9d80b (public).
The 7:37 daily run must treat 16 Nov as SCHEDULED (do not make another reel).

## Story (common audience, curiosity → answers), 151 s incl. end-card
Cold-open hook 0–2.8 s: fiery descent at the tower "ഇത് സിനിമയല്ല!" → plasma "26,794 km/h-ൽ space-ൽ നിന്ന് വീഴുന്ന rocket…" → title "Rocket-നെ tower പിടിച്ചു!"
Liftoff (33 engines) → how does it rise? balloon animation → Newton's third law over the climb → in space (onboard) → why doesn't it fall? Newton's cannon animation,
v = √(GM/r) ≈ 7.7 km/s, 1 round ≈ 90 min, ROUND 1→14 → 26 Starlink → reentry plasma 26,794 km/h (HUD), compression heating, heat shield →
belly-flop skydiver, air resistance, 540 km/h at 10 km (HUD) → flip + landing burn, thrust > weight (F = ma) → chopsticks catch, world first →
why reuse (cheap space; booster not caught this time) → quiz: rocket rises by which law? A) first B) third.
Checks: r = 6371+275 km → v = 7.74 km/s, T = 89.9 min; Kerala ~600 km / 7.7 km/s ≈ 78 s.

## Footage
JMK's screen recordings of the SpaceX webcast (15 Nov): c1 liftoff (X replay), c2 catch (YouTube re-upload of SpaceX feed), c3 Starlink deploy,
c4 reentry plasma, c5 belly-flop onboard. Frames extracted by extract_frames.sh (crop to 9:16 without the HUD) into /home/claude/sx/frames — not committed.
Raw clips not committed (large). No on-screen credit (JMK prefers none); caption credits "Video: SpaceX".

## Sources
- https://www.drohnen.de/97929/starship-flight-15-live-ship-catch-en/
- https://thespaceroad.com/articles/starship-flight-15-recap/
- https://www.teslaoracle.com/2026/11/13/watch-the-live-streams-of-starship-flight-15-with-live-updates/
- https://hotair.com/john-s-2/2026/11/14/heres-why-the-flight-15-booster-catch-was-abandoned-n3821015

## AI voice version (JMK asked 15 Nov 23:24)
- ElevenLabs eleven_v4, voice D6wSSgA3oM61Ljd71fAY, 1 generation, 2346 credits; transcription 0 credits. Script: starship_voice_lines.py (285 words, 144.7 s).
- FULL re-render timed to the word starts (tools/topics/starship_catch_vo.py + starship_words.json): every scene, caption, card and quiz beat follows the voice. Checked frames at 8 spoken words — caption on screen matches the spoken word.
- Files: starship_catch_aivoice_ig.mp4 / _yt.mp4 (~2:30). Voice wav tools/vo_starship.wav is gitignored; mp3 kept outside the repo.
- NOT POSTED yet: waiting for JMK's "ok". On ok: replace the media of both scheduled posts (IG post_b7ac3c056c7a50f9, YT post_46e08d83e2d9d80b) with the aivoice pair, add AI labels (IG isAiGenerated, YT containsSyntheticMedia) and "🔊 Voice-over: AI voice (my own cloned voice)" in the caption.
