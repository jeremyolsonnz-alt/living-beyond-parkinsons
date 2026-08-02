# Living Beyond Parkinson's — Pre-Launch Checklist

The single, current to-do list. The site is now **20 pages** with a script pipeline,
per-page See/Feel/Both toggles, an imagery self-check, six support pages, and a
`public/` vs `build/` deploy split. Items marked **[blocker]** should be done before
publishing; the rest can follow. Deploy detail lives in `README.md`.

---

## 1. What's done and verified (no action needed)

- **20 served pages** in `public/`: home, research, guided-imagery, the five practices, imagery-check, bibliography, work-with-jeremy, contact, the six support pages (newly-diagnosed, for-family-and-friends, when-nothing-happens, for-clinicians, glossary, feedback), plus thanks and 404.
- Navigation identical on every main page; footer "support & guidance" links on every page; colour palette and footer consistent throughout.
- No broken internal links anywhere; all HTML structurally balanced.
- Evidence badges consistent across every place each practice appears — **one Moderate (Walking Freely), four Emerging** — reflecting the 2025 null UPDRS-III meta-analysis.
- Every practice page carries its disclaimers (synthesis note, own-voice disclosure, anatomy warning, complement-not-replacement) and a working, persisted See/Feel/Both toggle.
- Bibliography verified against the published record, including the null result and the Malouin (KVIQ) citation behind the self-check.
- The `build/` toolkit is isolated from serving (Netlify publishes only `public/`).

---

## 2. Content placeholders to fill  **[blocker]**

Both are flagged on-page in dashed gold boxes.

- [x] **Contact email** — `jeremy@livingbeyondparkinsons.com` added to `public/contact.html` as a `mailto:` link. Placeholder note removed.
- [ ] **"Work with Jeremy" details** — in `public/work-with-jeremy.html`, add session format, availability, and any fees, or remove the section. Remove the placeholder note.

---

## 3. Audio  **[blocker for the practices to be "complete"]**

Each practice page has a disabled player with a placeholder filename (`audio_walking.mp3`, `audio_flow.mp3`, `audio_steady.mp3`, `audio_hand.mp3`, `audio_calm.mp3`).

- [ ] Record the five narrations. The exact scripts to read are auto-generated — run `python3 build/generate.py`, then use `build/out/audio/<id>.txt` (the agnostic wording). Jeremy records these directly in his own voice — no synthesised or AI-generated voice is used anywhere on this site.
- [ ] Add the five MP3s to `public/` (or a `public/audio/` folder — update the paths if so) and wire up each player (or swap in a simple `<audio controls>`).
- [ ] Keep the own-voice disclosure visible on each page (already written in).

---

## 4. Anatomy images  **[blocker]**

All five Phase II illustrations are cross-hatched placeholders with an on-page warning.

- [ ] Replace each with a correct diagram from **Servier Medical Art** (free, CC-licensed) or licensed stock. **Never use AI-generated anatomy.**
  - Walking Freely → basal ganglia / SMA gait loop (mesencephalic locomotor region)
  - Finding Flow → basal ganglia (striatum, globus pallidus, substantia nigra) + SMA loop
  - Steady Ground → vestibular system + proprioceptive / postural-control integration
  - The Steady Hand → motor-cortex hand region (homunculus) + basal-ganglia amplitude loop
  - Calm Beneath the Storm → vagus nerve / parasympathetic pathway
- [ ] Add image credits where the licence requires; remove the dashed warning caption once the real image is in.

---

## 5. Editing scripts later (the pipeline)

Script text is single-sourced in `build/scripts/<id>.json` (each paragraph has agnostic wording plus optional see/feel overrides).

- [ ] To change any script wording, edit its JSON, then run `python3 build/generate.py <id>`.
- [ ] Paste the refreshed `build/out/partials/<id>.script.html` into the matching page's script section (between the cue-toggle and the "pathway" section). The toggle CSS/JS already live in the page.
- [ ] The same run refreshes the audio script and the print (see/feel/both) files.

---

## 6. Deploy  **[blocker]**  — full steps in `README.md`

- [ ] Push the repo to GitHub; import it into Netlify (it reads `netlify.toml` and publishes `public/`).
- [ ] Point the domain via Cloudflare (proxied CNAME → `your-site.netlify.app`; SSL/TLS **Full (strict)**); enable HTTPS in Netlify.
- [ ] Replace `REPLACE-WITH-YOUR-DOMAIN` in `public/sitemap.xml` and `public/robots.txt` with the real domain.
- [ ] **Feedback form:** confirm Netlify Forms picks up `feedback.html` (it uses `data-netlify="true"`); test a submission lands in the Netlify dashboard and redirects to `thanks.html`. Moderate submissions there — never publish a quote unless the consent box was ticked.

---

## 7. Evidence integrity (final read-through)

- [ ] Re-read each practice's evidence note against its badge — nothing should read stronger than the badge allows.
- [ ] Confirm the research page still leads with the 2025 null on overall motor symptoms, and that Finding Flow reads as Emerging everywhere.
- [ ] Spot-check a few bibliography DOIs by clicking through.
- [ ] Confirm Calm still states imagery does not shorten "off" periods or change the medication cycle.

---

## 8. Language and tone

- [ ] Person-first language throughout ("people with Parkinson's").
- [ ] No "recovery" / "back to normal" language anywhere.
- [ ] The transparency note (Jeremy does not have Parkinson's) stays as written.
- [ ] The clinician page is intentionally technical; the rest are plain-language — leave that distinction as is.

---

## 9. Technical polish

- [ ] Add a `favicon` and Apple touch icon.
- [ ] Add Open Graph / social-preview tags (title, description, image) — the wordmark on cream works as the share image.
- [ ] Test on a real phone: hamburger menu, collapsible scripts, the See/Feel/Both toggle, and the self-check all work by touch.
- [ ] Run an accessibility checker (contrast, heading order, focus states — focus outlines and reduced-motion support are already built in).
- [ ] Keep the no-ads/no-tracking promise — if you want stats, use a privacy-respecting, cookieless option.

---

## 10. Support pages — quick review

- [ ] Read the six support pages once in a browser; confirm tone and links.
- [ ] Confirm the self-check "Set my practices to this" button and each page's toggle behave as expected (they share the `lbp-cue-mode` setting).

---

## 11. After launch (ongoing)

- [ ] Keep the bibliography current — update or remove a finding if stronger evidence contradicts it (the closing note already promises this).
- [ ] Revisit badges as trials mature; "Emerging" may change.
- [ ] Watch feedback submissions; fix anything flagged.
- [ ] Optional: align nav/palette with the sibling Living Beyond SCI and Stroke sites, and cross-link them.

---

*Static site: `public/` is served; `build/` is the toolkit and is never deployed. No build step, no database — hostable anywhere that serves files.*
