# Bug Resolver AI Agent

Bug Resolver AI Agent is a Flask-based application that helps developers go from bug report to actionable output faster. It accepts an issue description, generates a suggested Python fix, and generates unit tests for that fix using an LLM (Groq API).

The project includes:

- A web app with authentication and bug history.
- A simple CLI runner for quick local experimentation.
- A GitLab-style webhook endpoint for automated issue processing.

## Why this project matters

Debugging is not only about finding the error, it is also about writing reliable fixes and validating them quickly. This project is useful because it:

- Reduces turnaround time from bug report to first draft fix.
- Encourages test-first validation by always generating test cases.
- Keeps a per-user history of issues and generated outputs for traceability.
- Can be integrated into issue workflows through a webhook endpoint.

## Features

- User signup/login/logout.
- Dashboard to submit bug reports and view generated results.
- AI-generated Python fix suggestions.
- AI-generated unit test suggestions (`unittest` style).
- Saved chat/history entries in SQLite.
- Routes for profile/settings/developer pages.
- `/webhook` endpoint to process issue payloads.

## Project structure

```text
.
|- main.py                        # CLI entry point
|- database.py                    # SQLAlchemy models and DB setup
|- requirements.txt               # Python dependencies
|- agent/
|  |- issue_parser.py             # Converts raw issue text to structured input
|  |- fix_generator.py            # Calls Groq model to generate fix code
|  |- test_generator.py           # Calls Groq model to generate tests
|- gitlab/
|  |- webhook_listener.py         # Main Flask app and routes
|  |- templates/                  # Jinja HTML templates used by Flask
|- Project_Outcome/               # Demo screenshots/video assets
|- tests/                         # Test folder (currently empty)
```

## Tech stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Groq API (LLM inference)

## Prerequisites

- Python 3.10+
- A Groq API key

## Setup

1. Clone the repository and go to the project root.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Create a `.env` file.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment variables

Create `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_flask_secret_here
```

Notes:

- `GROQ_API_KEY` is required for fix/test generation.
- `SECRET_KEY` is recommended; if not provided, the app uses a fallback development secret.

## Run the application

### Option 1: Run the web app (recommended)

```bash
python gitlab/webhook_listener.py
```

Then open:

- `http://127.0.0.1:5000/login`

On first run, SQLite tables are created automatically.

### Option 2: Run the CLI agent

```bash
python main.py
```

You will be prompted to enter an issue text. The CLI prints:

- Generated fix suggestion
- Generated unit tests

## How to use (web flow)

1. Sign up a new account.
2. Log in.
3. On the dashboard, paste or write a bug description.
4. Click `Generate Fix & Tests`.
5. Review generated code and tests.
6. Open previous chats from the left sidebar.
7. Delete old chats if needed.

## Webhook usage

The app exposes `POST /webhook` to process issue events.

- Expected: payload containing `object_kind == "issue"` and `object_attributes` with `title` and `description`.
- Behavior: generates fix/tests internally and returns JSON status.

Example minimal payload:

```json
{
	"object_kind": "issue",
	"object_attributes": {
		"title": "Function returns wrong value",
		"description": "For negative input, result should be absolute value"
	}
}
```

## Current behavior and limitations

This is a hackathon-style prototype. Keep these points in mind:

- Passwords are currently stored in plain text (not production-safe).
- Prompt logic in generators is currently specialized for a specific function format (`function(x)` and absolute-value-style behavior), so outputs may not generalize for all bug types.
- There are no automated tests in the `tests/` directory yet.
- Error handling around external API failures can be improved.
- The webhook currently returns processing status but does not create merge requests or commit changes.

## Demo assets

Project visuals are available in `Project_Outcome/` (screenshots and video).

## Future improvements

- Add password hashing and stronger auth/session protections.
- Generalize prompt templates for broader bug classes.
- Add automated test suite and CI checks.
- Add retry/fallback handling for API timeouts.
- Integrate generated fixes with repository automation (MR creation, comments, patch suggestions).

## Author

- Anmol Shukla (as referenced in the developer page)

## License

No explicit license file is currently included in this repository.
