# Living Beyond Parkinson's

A free guided-imagery and wellbeing site for people living with Parkinson's disease.
Static HTML/CSS with a little JavaScript — no framework, no database, no build step required to serve it.

---

## Repository structure

```
.
├── public/                 ← THE WEBSITE (this is all that gets served)
│   ├── index.html
│   ├── research.html
│   ├── guided-imagery.html
│   ├── walking-freely.html, finding-flow.html, steady-ground.html,
│   │   the-steady-hand.html, calm-beneath-the-storm.html   (the 5 practices)
│   ├── imagery-check.html
│   ├── newly-diagnosed.html, for-family-and-friends.html,
│   │   when-nothing-happens.html, for-clinicians.html,
│   │   glossary.html, feedback.html, thanks.html            (support pages)
│   ├── bibliography.html, work-with-jeremy.html, contact.html
│   ├── 404.html, robots.txt, sitemap.xml
│
├── build/                  ← THE TOOLKIT (never served — see netlify.toml)
│   ├── scripts/<id>.json   ← single source of truth for each practice script
│   ├── generate.py         ← turns each JSON into audio scripts, print files, partials
│   └── out/                ← generated output (git-ignored; rebuildable)
│
├── netlify.toml            ← tells Netlify to publish ONLY public/
├── .gitignore
├── launch-checklist.md     ← pre-launch to-do list
└── README.md
```

The split is deliberate: **`public/` is the website; `build/` is the workshop.**
Netlify only publishes `public/`, so the script sources, the generator, and its
output are version-controlled but never exposed on the web.

---

## The single-source pipeline

Each practice's spoken script lives in **one** file: `build/scripts/<id>.json`.
Every paragraph has an `agnostic` wording (the default, and the audio narration)
plus optional `see` / `feel` overrides used by the on-page See/Feel/Both toggle.

Regenerate everything after editing a script:

```bash
python3 build/generate.py            # all practices
python3 build/generate.py walking-freely   # just one
```

This writes, into `build/out/`:

- `audio/<id>.txt` — narration script for recording (Jeremy's own voice, recorded directly)
- `print/<id>-both.html`, `-see.html`, `-feel.html` — print-ready (A4) → "Print to PDF"
- `partials/<id>.script.html` — the script block with `data-see` / `data-feel`
  attributes that gets pasted into the matching `public/<id>.html`

> After regenerating, paste the new partial into the practice page's script
> section (between the cue-toggle and the "pathway" section). The toggle JS and
> CSS already live in the page.

---

## Deploy — Option C: Cloudflare → GitHub → Netlify

This serves the site from Netlify, with the domain managed at Cloudflare.

1. **Push to GitHub.** Create a repo and push this project to it.

2. **Connect Netlify to the repo.** In Netlify: *Add new site → Import an existing
   project → GitHub → pick the repo.* Netlify reads `netlify.toml` and publishes
   `public/`. No build command is needed. First deploy gives you a
   `your-site.netlify.app` URL to test.

3. **The feedback form works automatically.** `feedback.html` uses Netlify Forms
   (`data-netlify="true"`). Submissions appear in your Netlify dashboard under
   *Forms* — nothing is shown on the site. `thanks.html` is the post-submit page.
   Moderate submissions there; never publish a quote without the consent box ticked.

4. **Point the domain via Cloudflare.**
   - Add your domain to Cloudflare (it becomes your DNS).
   - In Netlify: *Domain settings → Add a custom domain* → enter your domain.
   - In Cloudflare DNS, add a **CNAME** for your domain (or `www`) pointing to
     `your-site.netlify.app`, set to **Proxied**.
   - In Cloudflare **SSL/TLS**, set the mode to **Full (strict)**.
   - Back in Netlify, enable HTTPS (Let's Encrypt) once DNS resolves.

5. **Finish the sitemap.** Replace `REPLACE-WITH-YOUR-DOMAIN` in
   `public/sitemap.xml` (and the `Sitemap:` line in `public/robots.txt`) with your
   real domain.

Any future edit pushed to GitHub redeploys automatically.

---

## Before launch

See **`launch-checklist.md`** for the full list. The blockers only you can do:
add the contact email and "work with Jeremy" details, record the five audio
narrations, and replace the five anatomy placeholder images with correct
diagrams (Servier Medical Art or licensed stock — never AI-generated anatomy).

---

*Built by Jeremy Olson, Auckland, New Zealand. Free, no paywall, no email gate, no ads.*
