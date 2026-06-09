# Think Tank

Collaborative game idea voting platform for Code Platoon — Dakota Cohort.

Teams: **404 Brain not found!** and **Da_Koders**

---

## Setup (fork → run locally)

```bash
# 1. Clone your fork
git clone https://github.com/YOUR_USERNAME/think-tank
cd think-tank

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env — set a real SECRET_KEY (any long random string)

# 5. Run migrations
python manage.py migrate

# 6. Seed the default project
python manage.py seed

# 7. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000/project/1/

---

## Usage

1. Set your handle and pick your team (404 Brain not found! or Da_Koders)
2. Submit game ideas in the Recent Ideas feed
3. Suggest themes in the Theme Poll and vote on others

---

## Known bug (do not fix yet)
Duplicate idea submissions are not prevented — the same idea can be submitted multiple times. Flagged for a future fix.

---

## Stack
- Python 3 / Django 4.2
- SQLite (local dev)
- Vanilla JS + CSS (no build step)
