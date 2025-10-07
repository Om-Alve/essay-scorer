set shell := ["bash", "-c"]

[working-directory: "be"]
start-be: 
  source .venv/bin/activate
  uv run fastapi dev main.py

[working-directory: "fe"]
start-fe: 
  npm run dev

start:
  mprocs --names "backend, frontend" "just start-be" "just start-fe"

