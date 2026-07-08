# Verification Rules

## Structural Rules

- JSON outputs must validate against the schemas in `contracts/`.
- API route definitions must align with `contracts/api_contract.openapi.yaml`.
- Example artifacts must remain within the allowed scope in `PRODUCT_RULES.md`.

## Consistency Rules

- Repo plans must cover the responsibilities named in the project spec.
- Tasks must map to a repo target and owner role.
- Prompt packs must use the same scope boundaries as the spec.

## Frontend Rules

- The frontend must render source-of-truth artifacts directly.
- Missing fields should fail visibly, not be replaced with invented structure.

## Safety Rules

- Reject scopes that imply bots, account automation, emulator control, client memory access, or live service interference.
- Reject features that turn planning artifacts into hidden operational state.

## Red Team Targets

- scope inflation
- unsafe reinterpretation
- contract drift
- hidden frontend state invention
- unverifiable prompts
