# External Review Prompt

Use this prompt when reviewing `ai-assembly-line` from a fresh clone.

## Review Rules

- Treat the Git repository contents as the only source of truth.
- Do not rely on chat history, prior assistant claims, or out-of-band context.
- Review the repository as it exists on disk after cloning.

## Fresh-Clone Review Steps

1. Clone the repository and enter the repo root.
2. Read the top-level guidance first:
   - `README.md`
   - `PROJECT_SPEC.md`
   - `PRODUCT_RULES.md`
3. Inspect the contract and generated-state layers:
   - `contracts/`
   - `generated/`
4. Inspect the static viewer:
   - `web/`
   - `web/README.md`
   - `web/index.html`
   - `web/repos.html`
   - `web/backlog.html`
   - `web/prompts.html`
   - `web/slots.html`
   - `web/verification.html`
   - every `.js` file under `web/`
5. Inspect relevant docs under `docs/`.

## Validation Commands

Run these checks from the repository root:

```powershell
python tools\validate_seed.py
```

```powershell
Get-ChildItem web -Filter *.js | ForEach-Object { node --check $_.FullName }
```

If you want to review the static viewer in a browser, serve the repository root and open the viewer from `http://localhost:8000/web/`:

```powershell
python -m http.server 8000
```

## Review Focus

Confirm whether the repository currently behaves as a Phase 0 planning kernel and static read-only viewer.

Check for:

- source-of-truth drift between `README.md`, `PROJECT_SPEC.md`, `PRODUCT_RULES.md`, `contracts/`, `generated/`, and `web/`
- stale references to placeholder web surfaces that no longer exist
- viewer pages that claim behavior not backed by generated JSON
- frontend-owned models or invented workflow state
- schema drift or undocumented generated structure
- any accidental addition of backend behavior, authentication, databases, realtime sync, editing, or mutable dashboards

## Expected Reviewer Posture

- Be strict about traceability.
- Prefer concrete file references over high-level impressions.
- Treat missing validation, stale docs, and mismatched generated artifacts as review findings.
