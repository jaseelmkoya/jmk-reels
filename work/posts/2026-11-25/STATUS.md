# 2026-11-25 (Wed) · PYQ CAROUSEL — Prism refractive index derivation (Plus Two · Ray Optics)
SCHEDULED
- Feed (5-slide carousel) 25 Nov 20:30 IST: post_999e6fda70cf32ad (med_8e6105671c275b34, med_31eaafe8a04317f5, med_af345573c708c607, med_19c54c3b59039a60, med_7bf6ee8cb3ea6910)
- Story B (recap of the derivation) 26 Nov 07:30 IST: post_2a71eff5f7f6e9e3 (med_67f4534d4c10ace7)
- No reel/video mention anywhere. Last 14 days: EMI, black hole, projectile, work-energy → no repeat.
- Christmas season: Monday 23 Nov quiz was Plus One → this Wednesday PYQ is Plus Two (no earlier Wed PYQ post on record).
- Rebuild: copy tools/fonts (Anek Bold/ExtraBold/SemiBold, comic-neue 700) here, run build.py (renders to out/).
- add_repo tool was not offered this run; the repo was already cloned in the session and push worked.
## Accuracy check
- Label: plus-two-physics-christmas-pyq 2019 4-mark section (Q22–25), Q24 "Derive the refractive index of a prism, n = sin((A+D)/2)/sin(A/2)" → "PYQ · Plus Two Christmas Exam 2019 · Q24 (4 marks)" ✓
- Hook "7-ൽ 6": skill table rank 1 — prism in 2017, 2018, 2019, 2023, 2024, 2025 (not 2022) = 6/7 ✓; 2017 Q17 asked only "show A + δ = i + e" ✓
- Derivation vs plus-two-physics-material + NCERT: r₁ + r₂ = A (quadrilateral with 90° at both faces + triangle of normals), δ = (i−r₁)+(e−r₂) = i+e−A, at D: i = e, r₁ = r₂ = A/2 (ray parallel to base for an isosceles prism), i = (A+D)/2, n = sin i / sin r ✓
- Python: A=60°, D=30° → n = sin45/sin30 = 1.41421 = √2 ✓. Diagram drawn to true geometry (A=60°, n=1.5 → i=e=48.6°, D=37.2°, and formula gives back n=1.5000) ✓
- No corrections to the material needed. Final images re-read: subscripts r₁ r₂, δ, brackets in formula, Malayalam not cut, footer icons OK.
## Fix (JMK, 25 Nov)
- JMK: emergent ray was drawn going upward (wrong) — it must bend down towards the base. Fixed in build.py (emergent direction +18.6° below horizontal, true geometry), added the backward extension of the emergent ray meeting the incident extension, δ marked between them. Slides 1, 2 and Story B re-rendered.
- Old scheduled posts post_57f6f92a326ffa14 and post_ad955f616fad395c deleted; new ones scheduled at the same times (ids above).
- Lesson: in every prism diagram, check the emergent ray bends towards the base (deviation towards the base).
## Fix 2 (JMK, 25 Nov)
- Footer YouTube name changed from "@jaseelmkoyajmk" to "JMK Space" on all 6 images (JMK: YouTube name is JMK Space, never Jaseel M Koya).
- Posts post_40d40bc423fef212 / post_d1b3a00f70176308 deleted; rescheduled as above at the same times.
- Full re-check of all 6 final images: ray diagram (incident from below, bends towards normal inside, parallel to base, emergent bends away from normal towards the base, δ between incident extension and emergent back-extension, i/r₁/r₂/e measured from normals), every formula, label, year chip, Malayalam text and footer.
- Daily post task prompt updated: "JMK Space" everywhere, zero-mistake rule (JMK doesn't review before posting) and a DIAGRAM CHECK.
- Note: tools/endcard.py (reel tooling) still contains "jaseelmkoyajmk" — not changed here (reel task's area).
