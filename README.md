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

---

## Stack

- Python 3 / Django 4.2
- SQLite
- Vanilla JS + CSS — no build step required
