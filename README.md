# ACEest Fitness and Gym DevOps assignment

A foundational Flask API adapted from the supplied ACEest Tkinter examples. It preserves the Fat Loss, Muscle Gain and Beginner calorie factors (22, 35 and 26), client records and adherence tracking while replacing desktop widgets with HTTP endpoints. The original GUI versions are references, not container entry points.

## Local setup

Use Python 3.10+; CI and Docker use Python 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 on your Fedora laptop. See SETUP_GUIDE.md for college/personal GitHub separation, laptop setup and the course VM Jenkins build.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health status |
| GET | /programs | Program names and calorie factors |
| GET, POST | /clients | List or add clients |
| GET | /clients/NAME | Retrieve a client |
| POST | /clients/NAME/progress | Add integer adherence from 0 to 100 |

Example:

```bash
curl -X POST http://127.0.0.1:5000/clients -H 'Content-Type: application/json' \
  -d '{"name":"Demo","weight":70,"program":"FL"}'
```

The example calorie target is 1540. Invalid requests return 400, unknown clients return 404 and duplicate clients return 409. Records are held in memory and reset with the process. This lab app has no authentication or persistent database; use dummy data. Gunicorn runs one worker to keep the in-memory store consistent.

## Validation

```bash
python -m compileall -q app.py services.py tests
python -m ruff check --select E9,F63,F7,F82 app.py services.py tests
python -m pytest -q
```

## Docker

```bash
docker build -t aceest:local .
docker run --rm aceest:local python -m pytest -q -p no:cacheprovider
docker run --rm -p 127.0.0.1:5000:5000 aceest:local
```

The image uses Python slim, caches the dependency installation layer and runs as a non-root user. Test tools are included for assignment pipeline validation.

## Automation

GitHub Actions triggers on every push and pull request. It installs Python dependencies, compiles and lints code, builds the Docker image and runs tests inside that image.

Configure Jenkins as Pipeline from SCM with this public repository, branch */main and script path Jenkinsfile. The pipeline performs clean checkout, image assembly, syntax/lint validation and container tests. SCM polling checks main every five minutes after the first build registers the trigger. Its agent needs Docker access. This is build/test automation; no external production deployment or image publishing is configured.

## Actual execution evidence

Add your verified laptop and Jenkins VM versions, test count, GitHub Actions result/link and Jenkins build result/link here after running the project. Do not treat supplied configuration as proof that remote builds passed.

## Verified GitHub Actions Results

The GitHub Actions run for commit `518f051` successfully completed dependency installation, Python compilation, lint checks, Docker image assembly, and automated testing.

- Python compilation completed successfully.
- Ruff reported `All checks passed!`.
- Docker successfully built the `aceest-ci` image.
- Pytest ran inside the Docker container and reported `28 passed in 0.25s`.

