# Think Tank — VS Code Claude Handoff (v2)
**CORRECTION FROM LAST SESSION: This is a PROJECT think tank, not a game tank.**
**Do not frame anything around game development. This is a class collaboration tool.**

---

## FIRST MESSAGE — State Check
If continuing from a previous session, run this audit before doing anything:

```
Read every file in this project and report:
// FILES CHANGED THIS SESSION: [list]
// WHAT EACH CHANGE DID: [one line per file]
// WHAT STILL NEEDS DOING: [from the task list below]
// ANY BROKEN STATE: [imports missing, migrations not run, etc.]
Format as code comments. No prose.
```

---

## What This App Is
**A class project think tank / idea voting platform.**
- Students submit project ideas and vote on them
- Two student teams collaborate using the same instance:
  - **"404 Brain not found!"**
  - **"Da_Koders"**
- Running: Django @ `127.0.0.1:8000`
- URL structure: `/project/<id>/`

**This is NOT a game project. Do not add game-specific logic, game models, or game terminology.**

---

## STEP 0 — AUDIT (run before writing any code)

Read and report on:
```
models.py
views.py
urls.py
requirements.txt
templates/          ← list every .html file
settings.py         ← INSTALLED_APPS and DATABASE only
```

Report format:
```python
# models.py   — fields found: [list]
# views.py    — views found: [list]
# urls.py     — routes found: [list]
# templates   — files found: [list]
# missing     — [what the tasks below need that doesn't exist yet]
```

---

## TASK A — Team Separator

Add visual separation between the two teams in the Recent Ideas feed and Theme Poll cards.

**1. Add `team` field to handle/user model**
```python
TEAM_CHOICES = [
    ('404', '404 Brain not found!'),
    ('da_koders', 'Da_Koders'),
]
team = models.CharField(max_length=20, choices=TEAM_CHOICES, default='404')
```
Generate migration. Do not run it — let the dev run `python manage.py migrate`.

**2. Update Set Handle form**
Add a team selector (radio or dropdown). Required before submitting.

**3. Recent Ideas — team badge**
- "404 Brain not found!" → `#FF6B6B` (red/orange pill)
- "Da_Koders"           → `#00B4D8` (teal/cyan pill)
- Add filter toggle above feed: `[ All | 404 Brain | Da_Koders ]` (vanilla JS, no reload)

**4. Theme Poll cards**
Show `suggested by @handle · [team badge]` under each card title.

**Acceptance criteria**
- [ ] `team` field exists on model
- [ ] Handle form requires team selection
- [ ] Recent Ideas feed shows correct team badge
- [ ] Filter toggle works
- [ ] Entries without a team show "Unknown" badge gracefully

---

## TASK B — GitHub Integration

**Check `requirements.txt` first:**
- If `social-auth-app-django` is present → use Option B (OAuth)
- If not → use Option A (quick link, no OAuth)

### Option A — Quick (repo link + gh: handle prefix)
1. Add to `settings.py`:
```python
GITHUB_REPO_URL = os.environ.get("GITHUB_REPO_URL", "https://github.com/YOUR_ORG/YOUR_REPO")
```
2. Add to `context_processors` so it's available in all templates
3. Render in base template footer:
```html
<a href="{{ GITHUB_REPO_URL }}" target="_blank">🐙 View on GitHub</a>
```
4. Handle prefix: `gh:Username` shows a GitHub icon next to the handle in the UI

### Option B — Full OAuth
```
pip install social-auth-app-django
```
- Add `social_django` to `INSTALLED_APPS`
- Register GitHub OAuth App at github.com/settings/developers
- Add `SOCIAL_AUTH_GITHUB_KEY` and `SOCIAL_AUTH_GITHUB_SECRET` via `os.environ.get()`
- Replace handle input with "Login with GitHub" button
- Map GitHub username → handle automatically

**No secrets in settings.py. Use `os.environ.get()` for everything sensitive.**

---

## Known Bug (do not fix unless asked)
Recent Ideas shows duplicate entries — same idea submitted multiple times by the same user.
Likely missing duplicate check on form submit. Note it, don't touch it.

---

## Output Rules
- Diffs only — no full file rewrites unless file is under 30 lines
- Migrations: generate only, don't run
- No `print()` in production paths
- No inline styles — add CSS classes only
- No game-specific terminology, models, or logic

---

## Task Order
1. State check (if continuing session)
2. Audit → report
3. Task A: team separator
4. Task B: GitHub (Option A or B based on requirements.txt)
5. Log the duplicate bug, move on
