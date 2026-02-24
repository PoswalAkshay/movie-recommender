Render deployment and environment variables

1) Local development
- Copy `.env.example` to `.env` and set your TMDB API key:

  PowerShell:

  ```powershell
  Copy-Item .env.example .env
  ```

  Or on Windows cmd:

  ```cmd
  copy .env.example .env
  ```

- Install dependencies and run locally:

  ```bash
  pip install -r requirements.txt
  python app.py
  ```

2) Render (recommended)
- Push this repository to Git (GitHub/GitLab) and create a new Web Service on Render.
- In Render dashboard, open your service, go to **Environment** → **Environment Variables**, and add a secret:

  - Key: `TMDB_API_KEY`
  - Value: (your TMDB API key)

- `render.yaml` in the repo contains a placeholder entry. Render will use the dashboard secret at deploy time.

3) Notes
- Do NOT commit your `.env` to the repo. Use the dashboard to store secrets.
- The app uses `PORT` provided by Render; no manual `PORT` setting is required.
