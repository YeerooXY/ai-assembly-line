# CoC Base Builder Generated Project Spec

## 1. Safe Product Interpretation

Requested idea: "fully automatic base-builder app for Clash of Clans"

Accepted interpretation: an offline Clash of Clans base layout planner, editor, scorer, and simulator-style evaluator.

Rejected interpretations:

- botting or gameplay automation
- game client control
- account access
- emulator orchestration
- live service interaction

## 2. Product Summary

- Product name: CoC Base Builder
- Goal: help users design and compare base layouts outside the game
- Users: players, clan planners, guide authors
- Primary outcomes:
  - edit layouts on a grid
  - score layouts with transparent heuristics
  - save and load planner files
  - run offline simulation-style evaluation

## 3. Scope Boundaries

- Allowed:
  - offline planning
  - local save/load
  - heuristic scoring
  - route and coverage simulation
- Not allowed:
  - bot behavior
  - client hooks
  - memory reading
  - account login
  - emulator control
  - live service calls

## 4. Repo Split

- `coc-base-frontend`
  - render spec-derived state, layout editor, reports
- `coc-base-backend`
  - local-only file and evaluation API
- `coc-base-engine`
  - placement rules, scoring, path evaluation
- `coc-base-contracts`
  - schemas and fixtures

## 5. Domain Model

- `BaseLayout`
  - fields: `layoutId`, `townHallLevel`, `width`, `height`, `placements`, `metadata`
- `BuildingPlacement`
  - fields: `placementId`, `buildingType`, `x`, `y`, `rotation`
- `RuleSet`
  - fields: `ruleSetId`, `weights`, `penalties`, `version`
- `ScoreReport`
  - fields: `reportId`, `totalScore`, `subscores`, `warnings`
- `SimulationReport`
  - fields: `simulationId`, `coverageSummary`, `pathingSummary`, `notes`

## 6. API Contract Draft

- `POST /compile-layout`
  - validate and normalize a layout file
- `POST /score-layout`
  - return a score report for a layout
- `POST /simulate-layout`
  - return a simulation-style evaluation report
- `POST /save-layout`
  - save a local planner document
- `POST /load-layout`
  - load a local planner document

## 7. Frontend Screens

- Overview
- Layout Editor
- Score Report
- Simulation Review
- Saved Layouts
- Contracts and Verification

Rule: the frontend must render current project state from generated files and contracts. It must not invent its own task, repo, or contract structure.

## 8. Backend Services

- layout validation service
- score service
- simulation service
- local file save/load service
- fixture serving service

## 9. Core Engine Responsibilities

- bounds checking
- placement collision validation
- score computation
- simulation-style path and coverage analysis
- deterministic serialization
- warnings for invalid or weak layouts

## 10. Verification Tasks

- validate generated JSON against schemas
- test invalid placement fixtures
- test repeatable score outputs
- test simulation report structure
- verify frontend renders contract-defined artifacts only
- red-team automation or bot reinterpretation attempts

## 11. Copy-Paste Starter Prompts

### Planning Agent

Convert rough base-builder ideas into safe offline planner specs. Reject botting, automation, client control, account access, emulator usage, and live service integration.

### Contract Steward

Define strict schemas for layouts, reports, repo plans, and tasks. Keep the frontend contract-driven and reject undocumented state.

### Frontend Builder

Build views that render the current project spec and generated artifacts directly. Do not invent structure or UI-only task models.

### Backend Builder

Implement local-only HTTP routes matching the contract draft. No auth, database, cloud sync, or live service access.

### Core Engine Builder

Implement deterministic layout validation, scoring, and simulation-style evaluation for an offline planner only.

### Red Team Verifier

Probe for bot-like reinterpretation, client hooks, account workflows, schema drift, and frontend state invention.
