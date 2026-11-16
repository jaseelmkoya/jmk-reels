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
- YouTube cut (JMK 23:44): voice ends "Subscribe ചെയ്യൂ" (40-credit phrase spliced at 142.77 s, RMS-matched, 15 ms fade; vo_starship_yt.wav, gitignored), quiz text "Subscribe ചെയ്യൂ", then the SUBSCRIBE + bell end-card. Build with PLAT=yt. Instagram cut keeps "Follow ചെയ്യൂ" + Follow end-card.
- 16 Nov 08:18 JMK edits: Earth in the orbit animation = JMK's Earth image (tools/brand/earth.png); the "KE → heat" part uses JMK's brighter plasma clip (plasma_c, c6); the booster line now shows the booster landing burn over the sea (boost_burn) and the explosion (boost_boom, centred panel on blurred bg) from c7. extract_frames2.sh has the commands. All four files re-rendered (no-voice IG/YT, AI-voice IG/YT).
- 16 Nov 08:35: scheduled posts' media replaced with the updated no-voice files (IG med_aa31023c45f0bb50, YT med_59e84870960d7337). Still 18:30, still no voice until JMK says ok.
- 16 Nov 15:25 JMK: 'വോയിസുള്ള വീഡിയോ അപ്‌ലോഡാക്കിയാൽ മതി' → both scheduled posts now carry the AI-voice files (IG med_9863ef174b43d1ee, YT med_df6e8a73d0dfdd12 with Subscribe ending), AI labels on, caption line '🔊 Voice-over: AI voice'. Still 16 Nov 18:30.
- 16 Nov 16:06: Instagram cover = JMK's thumbnail (starship_catch_thumb_jmk.jpg, med_a970f9196e6f3033). YouTube Shorts take no custom thumbnail through the API.
- 16 Nov 16:55 JMK: YouTube unlisted at 5 PM, public at 6:30 (so he can set a custom thumbnail in between). YT post_46e08d83e2d9d80b published NOW as UNLISTED: https://www.youtube.com/watch?v=lCbdWUBL77k . Reminder trig_01TE9Aikb9umLUtvnJGLoswN at 18:30 IST switches it to public (update_post privacyStatus public). Instagram still scheduled 18:30.
