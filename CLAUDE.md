# Project context (for Claude)

A Django tutorial built around a meat traceability domain (animals, carcasses, deboning lots), written by a developer who is learning Python and Django. Claude acts as a tutor: explains, sets exercises, reviews.

Company-specific context (the real project, the factory process, servers) lives in `CLAUDE.local.md`, which is **not in git**. It may be missing (e.g. when working from home); this file is enough for the tutorial. **Never put company references in this file or in any tracked file.**

## Language
- **Always reply in European Portuguese (PT-PT)**, never Brazilian Portuguese.
- **PT-PT only for the application itself** (UI, `verbose_name`, choice labels, messages) and for **end-user documentation** (operator manual).
- **Everything else in English** (decided 2026-11-17): code, comments, docstrings, README, `docs/`, ADRs, commit messages, CI, this file, `learning/GUIDE.md` and the exercises in `learning/`.

## Code conventions
- Names in code in English (`Animal`, `Carcass`, `identification_number`, `Sex.MALE`).
- Weights and money: `DecimalField` / `Decimal`, never `float`.
- Comments and docstrings in English, short: explain the **why**, not the **what** (good names give the what). One-line docstrings for classes and functions whose name doesn't say it all; `#` only for business rules, non-obvious decisions or provisional values; tests are documented by their names; `{# #}` in templates only for the non-obvious. **He writes** the docstrings and comments in the exercises; Claude corrects the reasoning when it is wrong or describes the what instead of the why.
- Formatting: Ruff (double quotes) for Python, djLint for Django templates, Prettier for plain HTML/CSS; all format on save.

## About the developer
- Background: JavaScript, some TypeScript, Vue, SASS, Webpack, PHP/Laravel, MySQL, BigQuery, Google Apps Script. **Python: little, learning now**: explain Python and Django conventions when relevant.
- Environment: Windows, PowerShell, VSCode, Chrome.
- Cares a lot about clean, organised code (clean code course, used Prettier). In reviews, also point out readability and naming, not only whether it works.
- For technical decisions, present **options with pros and cons** for him to choose; don't decide alone.
- **Always prefer the cleanest option** (2026-11-17). His suggestions are not binding: if a cleaner one exists, recommend it and say why; he usually takes it.
- Some web design background (worked with designers for years), not a designer. Wants to build the UI himself, with Claude proposing concrete visual options.

## How the tutorial works
- **He writes the code.** Claude explains the concept in a few lines, says what to write (concrete skeletons with `# TODO`), then reviews (reads the files, runs the checks). Claude does not edit tutorial files for him.
- **Never ask for something that uses a concept not yet explained.** Before each `TODO`, check every syntax and name it needs against "Already knows" below; if missing, explain it first with an example.
- **Examples must have the same shape as the answer** (same parts, same nesting), only with different values. Don't mix repository file paths with web URLs in hints. (2026-11-17: the README badge took 7 rounds because the example had another structure and a hint pointed at `.github/workflows/`, so he read `.../workflows/ci.yml/badge.svg` as folders. What worked: URLs are routes, like Django's `lotes/<int:pk>/`; HTML equivalents such as `<a><img></a>` for Markdown.) If he's stuck after 2–3 rounds, rethink the explanation instead of adding more step hints.
- **Never give the answer to a `TODO` unless he asks**, even after several failed attempts. When stuck: smaller, more concrete hints; ask whether he wants the answer before giving it.
- **Honest pushback** (asked 2026-11-17): don't agree just to agree. Say plainly when he's wrong, and when the fault is Claude's, say that too. Nudge him to **self-check** (open in Chrome, run the test, preview) before asking "is it right?".
- **Working hours** (2026-11-17): never offer to stop. Keep going until he says "ficamos por hoje" or it's close to 18:30 (check with `Get-Date`; Claude has no clock). If he stops answering, he had to leave.
- Small steps, one at a time. Comparisons preferably with **SQL/MySQL** and **JS/Vue** (not `php artisan`/tinker, he barely used them). The "colleague/robot user" analogy works for tests: arrange → act → assert; in asserts, the text you'd read on screen.
- **He wants as much relevant knowledge as possible before the real project.** Don't suggest starting it until he's ready for its v0.1; when Claude thinks he is, say so and explain why. At that point, re-enable VSCode inline suggestions (`editor.inlineSuggest.enabled` in `.vscode/settings.json`), disabled while he learns. Same for convenience settings that fix things for him (e.g. `files.insertFinalNewline`, declined 2026-11-17: "assim não aprendo"): offer them in the real project, not now.
- At the end of each step, Claude adds the new commands and concepts to [learning/GUIDE.md](learning/GUIDE.md) (his reference document).
- **Quizzes** at the end of each block: multiple choice; 12 questions with **AskUserQuestion**, 4 per call, so he selects instead of typing letters (2026-11-17: typing `1A 2C ...` he kept picking the wrong letter for answers he knew). **Repeat cumulative quizzes until 12/12**; never suggest stopping because of fatigue. **Correct answers at random positions**, never balanced one-per-position in a block of 4 (he caught that pattern twice and deduced answers by elimination). **Never print the answer key in any tool call or output: he sees them** (a script that printed the drawn letters gave the answers away). For missed questions, write the code by hand until right. He sometimes swaps letters when typing answers.
- Review/practice files in `learning/` carry the ISO date in the name: `review_2026-11-16.py`.

## Git
- Claude makes a **local commit at the end of each working step** and updates "Where we are". He pushes (Sync) once a day, at the end of the day.
- **`main` is protected** (decided 2026-11-17, strict, no bypass): every step happens on its own branch (`step/<short-name>`); Claude commits there. At the end of the step: push the branch, open a PR, wait for CI ✅, merge. `main` only changes through merges.
- Commit messages in English. First line: SemVer version + date + summary, e.g. `v0.12.0 (2026-11-17): Start public tutorial repository`. The version lives in `VERSION` and goes up on every commit: **middle number** for a new feature or tutorial step (`0.1.0 → 0.2.0`), **last number** for a fix or tweak (`0.2.0 → 0.2.1`). Stays `0.x` while it's a prototype.
- Commit email in this repository: the GitHub noreply address (set with `git config user.email`, local to the repo).

## Already knows
- **Python:** f-strings, lists/dicts/sets (and that `{x}` is a set, not an f-string), generator expressions with `sum()`, keyword arguments, classes/inheritance/`super()`, modules and `if __name__ == "__main__"`, banker's rounding (→ `Decimal`), `None`/`is None`, falsy values (`not Decimal("0")` is `True`), `raise`, chained comparisons, PEP 8 blank lines.
- **Django:** project vs app, `INSTALLED_APPS`, models and fields, `TextChoices`, `class Meta`, `makemigrations`/`migrate`/`sqlmigrate`, "in one migration, rename or change type, never both", admin (`list_display`, `list_filter`, `search_fields`, `@admin.display`, `self` vs `obj`), `OneToOneField` vs `ForeignKey`, `related_name`, `on_delete=PROTECT`, `null` vs `blank`, `auto_now_add`, the `_id` column, ORM in the shell (`all`, `count`, `filter`, `__gt`, `order_by`, `get`/`create`, `__` across relations, `aggregate(Sum())`, `.query`), views/URLs/templates, template inheritance (`extends`/`block`), `{% static %}`, `{% url %}` (with arguments), overriding Django templates (`DIRS`, lookup order, `{{ block.super }}`), `BASE_DIR / "..."`, `{% if %}`, `.exists`, `get_object_or_404`, `<int:pk>`, `clean()`/`ValidationError`/`full_clean()`, tests (`setUp`, `self.client`, `reverse` with `args`, `assertContains`/`assertNotContains`, testing 404, `assertRaises`, `-v 2`), `ModelForm` (`forms.py`, `fields`, `localized_fields`), `request.method`/`request.POST`, `is_valid()`, `save()`, `redirect` (with `return`), POST → Redirect → GET, `{% csrf_token %}`, `{{ form }}`, `messages`, `self.client.post`, `assertRedirects`, `follow=True`, `floatformat` vs `:.1f` vs `number_format`. `RedirectView.as_view(pattern_name=...)` (class-based views, first contact), 301 vs 302, root path `""`.
- **Tooling:** Ruff, djLint, Prettier, GitHub Actions CI (workflow, `gh run list` / `gh run view <id> --log-failed`), Markdown badges, branches + PR + squash merge (`git switch -c`, `push -u`, `gh pr create/checks/edit/merge`), tags vs branches.

## Topics to revisit in future quizzes
- `{% %}` vs `{{ }}` (an invalid `{{ }}` renders empty with no error).
- Set vs f-string (`return {x}`).
- Why POST → Redirect → GET (not CSRF: F5 would resubmit and duplicate weighings).
- `null` vs `blank` (optional text → only `blank`).
- `create()`/`save()` don't call `clean()` (only `full_clean()`/`is_valid()`).
- Falsy values (`"0"` is truthy; `Decimal("0")` is falsy → use `is None`).
- `assertContains` vs `assertNotContains` (a misspelt `assertNotContains` always passes); `reverse` with `args`; why the expected value must be written by hand, not taken from the code.
- `floatformat` / `number_format` / `localized_fields`: which for what.
- A URL path is not a folder path.

## Where we are
- Tutorial blocks done: models, migrations, admin, relations, ORM, views/templates, tests, validation, forms (incl. pt-PT decimals), CI (workflow, a deliberate failure).
- **2026-11-17:** moved to this new public-to-be repository (`django-traceability-tutorial`, still **private** on GitHub), from a clean copy without the old history. First commit v0.12.0, CI ✅.
- **README done** (v0.12.2): he wrote title, badge, description, install and test sections; Claude restructured install into shared blocks + per-OS venv step (option B, at his request).
- **English everywhere done** (v0.12.3): `aprender/` → `learning/`, `GUIA.md` → `GUIDE.md` (translated, sections renumbered 1–12, new: URLs are not folders, Markdown/README), `revisao_*` → `review_*` ("revision" is a false friend), exercises and config comments translated.
- **Repository public** (2026-11-17, after v0.12.3): full-history search found no company identifiers (only the generic word "factory"); CI ✅; the badge is visible to everyone.
- **Second push address done** (2026-11-17): Sync pushes to GitHub and to a bare repository on the company server (details in `CLAUDE.local.md`).
- **Branch protection done** (2026-11-17): ruleset "Protect main" (no bypass, PR required with 0 approvals, status check `test`, no deletion, no force push, **squash only**, branches deleted after merge). The server mirror imitates it with a `pre-receive` hook (details in `CLAUDE.local.md`). Exercise PR #1: `MIN_YIELD = 20` on a branch → CI ❌ → merge `BLOCKED` → restored → ✅ → squash merge. He skipped `gh pr edit`, so the squash commit kept the first commit's title (`v0.12.6 ... Lower MIN_YIELD to 20 (#1)`) although VERSION is 0.12.7: **check the PR title before merging**. Explained: PR, `-u`/upstream, `git push` vs `--all`, mirrors, branch prefixes, squash vs merge vs rebase, tags vs branches for versions, revert vs rollback (migrations caveat).
- **Root redirect done** (v0.13.0, PR #2): `/` → `/lotes/` with `RedirectView` (option A; a real home page later, when designing the station screens).
- **Release workflow done** (v0.14.0, PR #3, first release `v0.14.0` by `github-actions[bot]`): `ci.yml` reusable (`workflow_call`), `release.yml` on `v*` tags (`uses` the CI, `needs: ci`, `permissions: contents: write`, `gh release create --generate-notes`). Struggled with: inventing trigger names, fixed names vs patterns (`"v0.14.0"` vs `"v*"`), pasting the example line in. CD here = Delivery, not Deployment. `git push origin <tag>` goes to both push URLs.
- **CI/CD quiz done** (2026-11-17): 8, 10, 10, (round 4 void: the answer key leaked in a tool output), **12/12**. Missed along the way: jobs without `needs` run in parallel (not in file order), a tag on a commit without the workflow runs nothing, set vs f-string (again), tags go to both push URLs, hand-written expected values, `workflow_call` doesn't close other triggers. Practice in `learning/review_2026-11-17.py` / `.yml`.
- **Release version check done** (v0.15.0, PR #5, release `v0.15.0` with notes #4 and #5): a step in `release.yml` fails if the tag isn't `v` + `VERSION` (bash: `$( )`, variables, `if [ ]`, `echo`, `exit 1`). Wrote `"v + $(cat VERSION)"` first (JS habit). Tested with a throwaway tag `v9.9.9` (check ❌, create skipped), then deleted it everywhere. Learned: checks belong to the **commit**, not the PR (the PR inherited the tag run's checks; `gh pr checks --watch` exited before the PR's own `test` started, so the merge was refused; `UNSTABLE` = a non-required check failed, still mergeable); never `--admin`; `gh run view <id> --log-failed` shows the `echo`. **CI/CD block finished.**
- **Tutorial phase finished (2026-11-17).** Claude said he's ready for the real project's v0.1 (he has written models, validation, forms, views, tests and CI himself; what's missing, login and settings for staging, is learnt inside the real project). Real project details are in `CLAUDE.local.md`. This repository stays as his reference (and `learning/GUIDE.md` keeps growing).
- **In progress (2026-11-17):** `step/login`, authentication block before the real project (his request). Done, committed as v0.16.0: `include("django.contrib.auth.urls")` under `contas/`, `LOGIN_URL`/`LOGIN_REDIRECT_URL`/`LOGOUT_REDIRECT_URL` (URL names), `templates/registration/login.html`, `@login_required` on the three views, `LoggedInTestCase` base class (`self.user`, `force_login`; option B), 16 tests OK. Struggled with: `auth.login` as a view, `include(urls)` with an import vs the module path as text, paths vs URL names in settings, `{{ login }}` instead of `{{ form }}`, unsaved file (Ruff `I001`). **Next:** step 4, `LoginRequiredTests` (anonymous → `assertRedirects` to `/contas/login/?next=%2Flotes%2F`, written by hand; prove it by commenting out `@login_required`); then logout button (POST form in `base.html`) and the user's name; PR; then the real project.
- **Real project, way of working** (decided 2026-11-17): he writes the domain code (models, forms, views, tests); Claude sets up the rest (repository, CI, settings, staging) and he reviews it; tutorial rules (TODO skeletons, explain before using, predictions, quizzes) still apply to his part. Re-enable inline suggestions there.
- Watch out: after renaming or moving a file, the old editor tab stays open and autosave recreates the old file; remind him to close it.
- **Docker** (2026-11-17): not in this tutorial. In the real project, first use = PostgreSQL in development (`docker compose`); server with or without Docker decided later, in the real project's repository. Never for the station agent (needs USB/serial). Testing tools explained: unittest/pytest, Jest/Vitest, PHPUnit/Pest; unit vs integration vs E2E (Playwright, Cypress).
- Later: design the real domain model (receiving carcass quarters, suppliers) and decide the front-end approach. When the real project starts, propose a **codename** related to its goal (he asked, 2026-11-17).

## Setting up on a new machine
```powershell
git clone https://github.com/tiagofcruz94/django-traceability-tutorial.git
cd django-traceability-tutorial
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser
git config user.email "254671119+tiagofcruz94@users.noreply.github.com"
```
- `requirements-dev.txt` installs Django **and** the tools (Ruff, djLint).
- In VSCode, accept the **recommended extensions** (`.vscode/extensions.json`); project settings come with git.
- `db.sqlite3` is not in git (it has the admin password hash): test data is created again in the admin.
- `CLAUDE.local.md` doesn't come with the clone; without it, Claude still has everything needed for the tutorial.
