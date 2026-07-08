# Project Specification Template

Use this template for future project-planning runs. Fill every section explicitly and keep generated artifacts aligned to `contracts/`.

## Product Summary

- Project name:
- Problem being solved:
- Target users:
- Core user value:
- Phase target:

## Safety / Legal / Platform Boundaries

- Allowed behaviors:
- Disallowed behaviors:
- Platform interaction limits:
- Data handling limits:
- Review or compliance notes:

## User Personas

- Persona name:
  - role:
  - goals:
  - pain points:
  - approval authority:

## Core User Flows

- Flow name:
  - trigger:
  - steps:
  - outputs:
  - failure modes:

## Non-Goals

- Explicitly excluded scope:

## Repository Split

- Repo or package name:
  - purpose:
  - owns:
  - depends_on:
  - excludes:

## Domain Model

- Entity name:
  - fields:
  - relationships:
  - validation notes:

## API Surface

- Endpoint or interface:
  - method_or_type:
  - path_or_name:
  - input_shape:
  - output_shape:
  - boundary notes:

## Frontend Screens

- Screen name:
  - primary user:
  - renders_from:
  - allowed interactions:
  - states:

## Core Engine Responsibilities

- Deterministic logic:
- Validation rules:
- Transformation rules:
- Scoring or evaluation rules:
- Export or compilation rules:

## Backend Responsibilities

- Read-only or write responsibilities:
- Validation responsibilities:
- Integration boundaries:
- Explicit exclusions:

## Verification Strategy

- JSON and schema validation:
- Contract validation:
- Fixture coverage:
- Negative testing:
- Human review gates:

## Red Team Attack Plan

- Misuse case:
  - attacker goal:
  - exploit path:
  - expected rejection or guardrail:
  - verification artifact:

## Microtask Backlog

- Task id:
  - title:
  - owner role:
  - depends_on:
  - outputs:
  - acceptance criteria:

## Agent Prompt Pack

- Prompt id:
  - role:
  - target repo:
  - allowed files:
  - forbidden files:
  - required context:
  - required outputs:
  - verification required:

## Definition of Done

- The project spec is internally consistent.
- Machine-readable outputs validate against `contracts/`.
- The planned frontend consumes generated state instead of inventing structure.
- Unsafe or out-of-scope interpretations are rejected or safely reinterpreted.
- Human reviewers can trace repos, tasks, prompts, and verification work back to this spec.
