# Weighted Product Discovery Order

AI Assembly Line keeps the internal lifecycle name `intake`, but presents the activity to users as **Product Discovery**.

The purpose is not to ask every imaginable question. The purpose is to reduce uncertainty in the right order.

## Core principle

```text
Define what we are building
  -> define who it is for
  -> define what those users do
  -> resolve the largest scope and architecture cuts
  -> define the MVP boundary
  -> define required product systems
  -> select the stack that best supports the accepted product
```

Do not choose technology first and then bend the product around it unless the user has a genuine non-negotiable technical constraint.

## Highest-information question rule

At every turn, ask the unresolved question with the greatest expected effect on:

- product identity;
- target users;
- MVP size;
- architecture;
- operating cost;
- safety or compliance;
- platform support;
- later refactor risk;
- team parallelization.

Do not continue into lower-level feature details while a higher-weight branching decision remains unresolved.

## Decision layers

### Layer 0 — Repository and lifecycle

Establish the durable product repository and active lifecycle phase.

Typical questions:

- Greenfield, existing repository, or planning-only?
- Which repository owns the product?
- Is the repository ready for branch and PR work?

### Layer 1 — Product identity

Determine the broad product category and intended maturity.

Typical questions:

- Game, mobile app, desktop app, web app, SaaS, API, library, CLI, firmware, embedded system, or another category?
- New standalone product or extension of an existing one?
- Research prototype, portfolio project, internal tool, MVP, production product, or commercial release?
- What outcome makes the product worth building?

### Layer 2 — Target users

Target users are a first-class design input, not a final marketing detail.

Determine:

- primary and secondary user groups;
- consumer, enterprise, internal, developer, education, family, specialist, or general audience;
- novice, casual, experienced, or expert skill level;
- solo user, household, team, organization, or public community;
- expected devices and environments;
- expected session length or workflow frequency;
- accessibility, age, language, and reliability expectations;
- the problem, desire, or experience the users are seeking;
- what success looks like from their perspective.

When user groups conflict, force an explicit priority or define distinct modes. Do not claim a product is for everyone without explaining how the experience adapts.

### Layer 3 — Core experience or workflow

Define what the user repeatedly does.

For games, this may include:

- primary gameplay loop;
- player fantasy;
- session and campaign structure;
- mastery, competition, cooperation, or narrative emphasis.

For applications, this may include:

- input;
- transformation or workflow;
- output;
- collaboration;
- review and decision points;
- frequency and urgency of use.

The core experience should be explainable in a few sentences before detailed systems are discussed.

### Layer 4 — Scope-cutting decisions

Resolve the decisions most likely to multiply implementation scope.

Ask when relevant:

- Offline, online, or hybrid?
- Single-user, multi-user, local multiplayer, online multiplayer, or asynchronous collaboration?
- Local-first, cloud-first, or synchronized?
- Real-time or turn-based?
- Handcrafted, generated, or hybrid content?
- Persistent world or discrete sessions/projects?
- One platform or cross-platform?
- Anonymous use, local profiles, full accounts, or organization identity?
- Third-party integrations or standalone operation?
- User-generated content, modding, scripting, or fixed product behavior?
- Regulated, safety-critical, privacy-sensitive, or ordinary-risk use?

These questions normally outrank detailed features because one answer may remove entire technical subsystems.

## Universal scope split

For any game or interactive application, explicitly resolve both dimensions when relevant:

1. **Connectivity:** offline, online, or hybrid.
2. **Participation:** solo/single-user, local multi-user, asynchronous multi-user, or real-time multiplayer/collaboration.

Do not treat “online” as synonymous with “multiplayer.” A single-player product may use online leaderboards, cloud sync, or content delivery. A multiplayer product may be local and fully offline.

### Layer 5 — MVP boundary

Only after product identity, users, core experience, and major scope cuts are understood, define:

- must-have behavior;
- minimum complete content;
- explicit postponed scope;
- non-goals;
- acceptance signals;
- release target and proof expectations.

Protect the MVP aggressively. A feature that is attractive but does not prove the core value should normally be postponed.

### Layer 6 — Product systems

Now resolve the systems required by the accepted MVP.

Examples:

- saves and persistence;
- progression and economy;
- permissions and roles;
- combat, enemies, inventory, or levels;
- notifications;
- search and filtering;
- import/export;
- analytics visible to the user;
- accessibility and settings;
- failure recovery;
- administration;
- payments or monetization.

Ask system questions from largest behavior and data implications down to local UX details.

### Layer 7 — Technology and architecture constraints

Choose the stack only after the product is sufficiently defined.

Before making a recommendation, confirm:

- target platforms;
- connectivity and participation model;
- performance needs;
- persistence and data model;
- deployment and operating expectations;
- required integrations;
- team skills and constraints;
- proof and testing needs;
- likely post-MVP expansion.

Technology selection should be a consequence of accepted requirements, not a substitute for them.

## Decision weight

Use these weights as guidance, not rigid arithmetic.

### Weight 5 — Identity and architecture multipliers

Examples:

- target users;
- product category;
- offline/online;
- solo/multi-user/multiplayer;
- target platform;
- regulated or safety-critical use;
- real-time synchronization;
- required external platform or hardware.

Ask these first when unresolved.

### Weight 4 — MVP shape and major operating model

Examples:

- campaign, sandbox, workflow, marketplace, or service model;
- handcrafted vs generated content;
- account model;
- persistent progression;
- monetization;
- release and distribution model;
- primary accessibility needs.

### Weight 3 — Major product systems

Examples:

- saves;
- economy;
- inventory;
- permissions;
- notifications;
- leaderboards;
- collaboration history;
- reporting;
- admin tooling.

### Weight 2 — Local mechanics and UX behavior

Examples:

- weapon slot count;
- checkpoint behavior;
- filter layout;
- editor interaction patterns;
- individual screen flows.

### Weight 1 — Polish and cosmetic detail

Examples:

- minor animation choices;
- exact colors;
- decorative feedback;
- low-risk labels and presentation details.

Do not ask Weight 1 or 2 questions while an unresolved Weight 5 question can invalidate their answers.

## Adaptive ordering

The layer order is a default, not a questionnaire script.

Skip questions already answered by the user. Raise a lower-layer question temporarily when it is necessary to clarify a higher-layer answer. Return to the highest unresolved layer afterward.

Do not ask irrelevant questions merely to complete a template. For example, a local CLI may not need multiplayer questions, while a collaborative editor certainly does.

## Project DNA

At the end of Product Discovery, generate a concise north-star artifact:

```text
assembly/intake/PROJECT_DNA.md
```

It should summarize:

- product type;
- project maturity and goal;
- primary and secondary users;
- user problem or desired experience;
- core workflow or gameplay loop;
- participation model;
- connectivity model;
- primary platforms;
- MVP boundary;
- explicit non-goals;
- guiding product principles;
- selected stack or technical constraints, only after selection.

Project DNA is a human-readable summary derived from accepted intake. It does not replace `project_intake.json` or `REQUIREMENTS.md`.

## “Engineerically vibing”

Creative exploration is welcome, but each accepted decision should reduce uncertainty rather than casually expand scope.

A good Product Discovery conversation feels open and energetic to the user while behaving like a disciplined decision tree underneath:

- largest branching questions first;
- one accepted choice at a time;
- tradeoffs visible;
- decisions persisted;
- scope reduced deliberately;
- technology selected last enough to be informed, but early enough to expose feasibility risks.
