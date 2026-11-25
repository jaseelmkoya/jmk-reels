# 2026-11-25 (Wed) · PYQ CAROUSEL — Prism refractive index derivation (Plus Two · Ray Optics)
SCHEDULED
- Feed (5-slide carousel) 25 Nov 20:30 IST: post_40d40bc423fef212 (med_21bb16eb8b0b4f02, med_cfdc4dc6bd737b90, med_be3f89848e225b3e, med_1ed046440e4f6fa7, med_65668708ef080e0a)
- Story B (recap of the derivation) 26 Nov 07:30 IST: post_d1b3a00f70176308 (med_f214c06e95ac8acf)
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
