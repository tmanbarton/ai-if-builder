# CLAUDE.md

Guidance for Claude Code when working in this repo. See `README.md` for project overview, structure, and tech stack.

## Environment

- Python 3.10+. Always assume the venv must be active before running `python` or `pytest`:
  ```bash
  source venv/bin/activate
  ```
- `ANTHROPIC_API_KEY` must be set in the environment for any code that calls the Claude API.
- Don't add new dependencies without asking first. If a new package is needed, propose it and wait for approval.

## Common commands

- Run tests with `python -m pytest <path> -v 2>&1 | tail -15`. Using `python -m pytest` (rather than bare `pytest`) ensures the venv's interpreter is used and the project root is on `sys.path`. The `-v` gives per-test status and `tail -15` keeps output manageable while still showing failures and the summary.
  - All tests: `python -m pytest tests/ -v 2>&1 | tail -15`
  - Single file: `python -m pytest tests/backend/test_database.py -v 2>&1 | tail -15`
  - Single test: `python -m pytest tests/backend/test_database.py::test_insert_duplicate_key_raises -v 2>&1 | tail -15`
  - If a failure is truncated, re-run with a larger `tail -N` or without the pipe to see the full traceback.
- Start the dev server: `uvicorn backend.endpoint:app --reload`

## Coding conventions

- **Always write a docstring for every new function, including tests.** Use reST/Sphinx style to match existing code:
  ```python
  def foo(bar: str) -> int:
      """
      Short summary of what the function does.
      :param bar: What this parameter is for.
      :return: What is returned.
      """
  ```
  ```python
  def test_foo(bar: str) -> int:
      """
      Short summary of what the test does. NOT a restatement of the function name. Don't include docstring if the test name is enough.
      """
  ```
- **Use type hints** on function signatures and on local variables where the type isn't obvious from context. Existing code does this consistently (e.g. `session_id: str = ...`, `locations: list[Location] = ...`).
- **snake_case** for functions, variables, and modules. **PascalCase** for classes. **SCREAMING_SNAKE_CASE** for module-level constants.
- Prefer f-strings for string formatting.

## Where things go

- **Pydantic data models** → `backend/models/` (one class per file, mirrors existing layout). Use `pydantic.BaseModel` and `Field(description=...)` when the field is part of a Claude structured-output schema.
- **Agent tool definitions** → `backend/tools/`. Tool schemas live in `tools/definitions.py`; new tools must be registered there.
- **Anything that talks to SQLite** → goes through `backend/database.py`. Don't open `sqlite3.connect` directly elsewhere.
- **Tests** → mirror the source path under `tests/` (e.g. `backend/database.py` → `tests/backend/test_database.py`). Test files are `test_*.py`, test functions are `test_*`.
- **MD Files for Tracking Progress** → `.claude/progress-trackers/` In-progress todos are here, and new ones go here as the user requests or you determine.

## Testing

- **Mock the Anthropic client** in tests. Don't make real API calls — it costs money and makes tests flaky.
- Use `tmp_path` fixture for any test that touches the filesystem or SQLite (see `tests/backend/test_database.py` for the pattern).
- **Skip tests of library behavior** (Pydantic, sqlite3, FastAPI internals) and tests that just re-walk a loop body already covered by another test. Test the project's own logic, not the framework's.

## Things to avoid

- Don't modify `venv/`, `examples/`, or generated output.
- Don't catch exceptions just to silence them — let them propagate unless there's a real recovery path.
- Don't refactor unrelated code while making a fix. Keep changes scoped to what was asked.

## Notes for working with the user

- The user is an experienced Java developer learning Python through this project. When introducing Python-specific patterns (decorators, context managers, comprehensions, `with` blocks, Pydantic, etc.), briefly explain what's happening rather than just using them silently. Prefer explaining and guiding over writing large blocks of code. Consult memory for information on this.
- Don't be afraid to confront/correc the user. The user may have a misunderstanding/have a concept wrong and is might try to correct you incorrectly.
