# Portfolio Website — Flask + Tailwind CSS

A production-ready developer portfolio for a FinTech & ML Software Developer.

## Tech Stack
- **Backend:** Python 3.11 + Flask 3.0
- **Frontend:** Tailwind CSS (CDN) + Vanilla JS
- **Templates:** Jinja2
- **Database:** SQLite (contact form messages)
- **Deployment:** Render / Railway

## Project Structure
```
portfolio/
├── app.py              # Flask app, routes, DB
├── data.json           # All content (projects, skills, experience)
├── requirements.txt
├── Procfile            # For Render/Heroku
├── render.yaml         # Render zero-config deployment
└── templates/
    ├── base.html       # Navbar, footer, dark mode, scripts
    ├── index.html      # Home / hero page
    ├── about.html      # About + skills
    ├── projects.html   # Projects grid with filtering
    ├── project_detail.html
    ├── experience.html # Timeline
    ├── contact.html    # Contact form
    └── 404.html
```

## Run Locally

```bash
# 1. Clone / copy the portfolio folder
cd portfolio

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Visit: http://localhost:5000

## Personalise

Edit `data.json` to update:
- Your name, bio, email, GitHub, LinkedIn
- Projects (add/remove/edit)
- Skills
- Experience entries

## Deploy to Render (Free)

1. Push code to a GitHub repository
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click Deploy
5. Your site is live at `https://your-app.onrender.com`

**Note:** Render free tier spins down after 15 min inactivity. First visit after sleep takes ~30 seconds.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask session secret | `dev-secret-change-in-production` |
| `PORT` | Server port | `5000` |

Set `SECRET_KEY` to a random string in production (Render generates one automatically via `render.yaml`).

## Features
- ✅ Fully responsive (mobile + desktop)
- ✅ Dark/Light mode toggle with localStorage persistence
- ✅ Smooth scroll reveal animations
- ✅ Project category filtering (ML / FinTech / Data / Web)
- ✅ Contact form with Flask validation + SQLite storage
- ✅ Custom cursor + navbar scroll effect
- ✅ 404 error page
- ✅ SEO meta tags
- ✅ Production-ready with Gunicorn
