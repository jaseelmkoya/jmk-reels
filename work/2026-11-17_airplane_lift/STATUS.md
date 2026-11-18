# 2026-11-17 · Why aeroplanes fly — Bernoulli + Newton's third law (Plus One · Mechanical Properties of Fluids)
Status: READY, NOT SCHEDULED — scheduled 17 Nov 18:30 then cancelled the same morning (JMK: post the J.C. Bose reel today instead). Uplika is connected again.
Topic came from topic_ideas.md NEXT (YouTube Studio idea, 15 Nov), so no news research this run.

## Reel (94 s + 4 s end-card, no voice) — v3 (JMK: also explain WHY pressure drops above the curve: air can't leave the wing (vacuum), curved path needs centripetal force, only pressure can push → atmospheric above, lower near wing). v2, 17 Nov: JMK asked to explain WHY the air is faster on top (up to 3 min is fine)
New scenes: streamlines squeezed over the wing → equation of continuity A₁v₁ = A₂v₂ (hose pipe); curved path needs a net force → low pressure above, high P in front pushes air into it → speeds up.
Hook "500 TONNE FLYING?" (A380 take-off) → "equal transit time" myth: top parcel reaches the trailing edge first →
Bernoulli card (P + ½ρv² + ρgh = constant), LOW P / HIGH P, LIFT → downwash: action (wing pushes air down) / reaction (air pushes wing up) →
quiz: Bernoulli's principle comes from conservation of A) energy B) momentum (answer A; PYQ: Plus One Model Exam 2020 — label added 17 Nov after JMK asked).
Files: airplane_lift_ig.mp4, airplane_lift_yt.mp4, airplane_lift_cover.jpg, captions (IG/YT), youtube txt, voiceover script, airplane_lift.py.

## Fact check
- Equal transit time is a myth; air over the upper surface arrives first (NASA Glenn "Incorrect Lift Theory"; https://pilotinstitute.com/the-curious-story-of-airplane-lift/).
- Lift = pressure difference + flow turning (downwash, Newton's 3rd law).
- A380 max take-off mass ≈ 575 t → "500 ടണ്ണിലേറെ".

## To post (after Uplika reconnect)
IG: accountIds ["conn_ab2a55cfffecc11d"], _ig.mp4, contentType reel, coverMediaId = cover, content = airplane_lift_caption.txt.
YT: accountIds ["conn_a84a14b4318a8e68"], _yt.mp4, title/tags from airplane_lift_youtube.txt, content = airplane_lift_caption_yt.txt, public, categoryId 27, ml, madeForKids false.
Or: set the sheet row's O/P date+time and Status "Post ചെയ്യാം" → the 17:00 task posts it.

## v4 — JMK's Google Flow clips mixed in (17 Nov)
JMK sent 11 Flow clips (prompts in flow_prompts.md). Checked each one:
- USED: take-off (hook, freeze + LIFT/WEIGHT arrows), hose pipe (continuity, freeze + thumb ring + v arrow), vapour over the wing 1–3.5 s (Bernoulli scene, LOW P/HIGH P/LIFT + "mist = low pressure-ന്റെ തെളിവ്"), wind tunnel (Newton 3rd action, ↓ arrows on the deflected air), cloud trough rear view (reaction ↑ arrow), sunset cruise (quiz background).
- NOT USED: stone on a string (no string visible, stone jumps — wrong physics; our own animation kept); second hose (hand disappears); first vapour clip (cartoon curls, strange smoke on runway); side-view cloud clip (no clear trough; rear view is better); window take-off (not needed).
- Vapour clip used only 1.0–3.5 s (after 4 s the mist turns into unnatural curls).
- Raw clips not committed (large, ~100 MB): frames are extracted to <workdir>/clips/<name>/ at 30 fps (CLIP_T0 in airplane_lift.py gives the start times: c1 1.5 s, c2 1.0 s, c8 1.0 s, c10 3.0 s, c11 3.0 s, c5 0 s).
- Cover now uses the real take-off frame (5.5 s).
- 18 Nov 00:0x: JMK sent a new stone-on-string clip (side view). NOT USED: from ~1.5 s the boy's hand is open (palm and fingers spread) while the string keeps whirling from his fingertips — nobody is holding the string, so the physics is wrong. Asked JMK for a regenerate (fist gripping the string, high 3/4 angle).

## v5 — AI voice (18 Nov, JMK: "ഓഡിയോ ElevenLabs-ൽ നിന്ന് എടുത്തോളൂ")
- ElevenLabs eleven_v4, JMK's clone voice D6wSSgA3oM61Ljd71fAY, 1 take, mood tags per section (1,733 credits). Flow xtH3iYck2Ztc78zi8vtG.
- JMK heard "vacuum" read as "വക്കം" → that sentence regenerated with Malayalam spelling "വാക്വം" (55 credits) and spliced in at 35.02 s (+0.83 s). Word times: eleven_scribe_v1 (0 credits), in airplane_lift_vo.py.
- JMK re-sent the Flow clips (18 Nov 10:56): c1 take-off, c2 hose, c8 vapour (the one with curls after 4 s), c10 wind tunnel, c11 cloud trough rear, c5 sunset; also the window take-off and the first vapour clip (unused). Frames extracted at 30 fps outside the repo.
- Full re-render timed to the words (airplane_lift_vo.py; PLAT=yt for YouTube: "Subscribe ചെയ്യൂ" said and shown). Quiz beats on the voice; PYQ label unchanged (Plus One Model Exam 2020).
- FINAL: airplane_lift_aivoice_ig.mp4 (100.4 s) / airplane_lift_aivoice_yt.mp4 (100.9 s), -16 LUFS. No cover made (JMK makes covers himself from 18 Nov).
- Voice wavs not committed. NOT scheduled — waiting for JMK's ok. When posting: AI labels on (aiGenerated, isAiGenerated, containsSyntheticMedia).
- 18 Nov 11:12: YouTube uploaded UNLISTED (JMK) — https://www.youtube.com/watch?v=iMGHx4ckXic (post_c6f29d49522d51ba, AI label on). JMK: post tomorrow (19 Nov) — Instagram + make YouTube public then.
