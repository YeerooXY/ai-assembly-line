# Roles

## Planning Agent

Turns rough ideas into structured product specs and decomposition artifacts.

## Contract Steward

Maintains schemas, contract compatibility, and fixture validity.

## Frontend Builder

Builds read-only static frontend views for Phase 0 that render generated planning state and contracts without inventing structure.

## Backend Builder

Implements API surfaces described by the OpenAPI contract when a later phase allows it.

## Core Engine Builder

Implements deterministic planning-kernel logic and validators for the current seed repository.

Domain-specific scoring or simulation-style evaluation belongs to future or example-specific work, such as `examples/coc-base-builder/`, not the current Phase 0 planning kernel.

## Red Team Verifier

Tries to trigger scope drift, safety failures, undocumented state, and weak verification logic.

## Human Reviewer

Approves scopes, boundaries, and planning outputs.
