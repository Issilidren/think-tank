# Think Tank

A collaborative idea voting platform for Code Platoon — Dakota Cohort.

Two student teams — **404 Brain not found!** and **Da_Koders** — use this to submit project ideas, suggest themes, and vote on what to build next.

---

## What it does

- **Set your handle** — pick a name and choose your team
- **Submit ideas** — drop project ideas into the shared feed; each one is tagged with your team
- **Filter by team** — toggle the feed to see All, 404 Brain, or Da_Koders ideas only
- **Theme Poll** — suggest a project theme and vote on others; one vote per person per theme
- **See who suggested what** — every poll card shows the handle and team that pitched it

---

## Getting started (fork this repo)

```bash
git clone https://github.com/YOUR_USERNAME/think-tank
cd think-tank

python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # open .env and set a SECRET_KEY

python manage.py migrate
python manage.py seed
python manage.py runserver
```

Open **http://127.0.0.1:8000/project/1/**

### Frontend (Vite)

Install frontend deps once:
```bash
cd frontend && npm install && cd ..
```

**Dev (hot reload)** — run both in separate terminals:
```bash
# Terminal 1 — Django
python manage.py runserver

# Terminal 2 — Vite dev server (hot reload)
cd frontend && npm run dev
```

**Production build** — bundle CSS/JS before deploying:
```bash
cd frontend && npm run build
```
Vite writes hashed assets into `static/dist/`. Django/whitenoise serves them.

---

## Stack

- Python 3 / Django 4.2
- Vite 5 (asset bundler, hot reload in dev)
- SQLite
- Vanilla JS + CSS
