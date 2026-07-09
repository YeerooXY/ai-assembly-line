# Multiplayer 2D Car Racing Game — Planning Package v0.1

## 1. Project intake summary

### Project name

Working title: **Car Game MVP**

Final name: open.

### Goal

Build a **desktop-first multiplayer 2D car racing game** with a serious client/server architecture and a small but complete first playable MVP.

The project should also serve as a portfolio-quality example of:

* Unity desktop client development
* UDP real-time multiplayer
* authoritative .NET game server design
* client prediction and reconciliation
* multi-repo, multi-agent project decomposition
* CI-published shared packages
* Docker-based deployment
* later Kubernetes readiness

### Target experience

Players launch a Windows client, enter a nickname, join or create a room, pick a car, ready up, and race against other players on a shared 2D track.

The driving should feel responsive and “fairly good,” not like a slow synchronized board game. Responsiveness matters.

---

## 2. MVP definition

### First official MVP

The first official MVP is a **complete tiny race game**, not just a technical demo.

It includes:

* Windows Unity client
* nickname-only player identity
* lobby room list/create/join flow
* short-lived join token
* UDP connection to authoritative game server
* 2–4 players per race room
* car selection from JSON-configured cars
* ready-up state
* countdown
* simple lap/checkpoint race
* finish/results screen
* one JSON-authored track
* deployment to an existing Linux machine using Docker Compose
* LAN/VPN test first
* public port forwarding later

### Explicitly excluded from MVP

The MVP does **not** include:

* accounts
* persistent profiles
* leaderboards
* matchmaking
* ranked play
* chat
* garage/customization
* multiple tracks
* fancy VFX/sound polish
* mobile support
* Linux/macOS clients
* Kubernetes runtime requirement
* anti-cheat beyond basic token validation
* advanced replay/ghost systems

---

## 3. Key architecture decisions

| Area                     | Decision                                         |
| ------------------------ | ------------------------------------------------ |
| Platform                 | Desktop-first                                    |
| First client OS          | Windows                                          |
| Client engine            | Unity                                            |
| Server                   | Separate C#/.NET authoritative server            |
| Multiplayer model        | Simple online rooms                              |
| Game mode                | Simple race mode                                 |
| Transport                | UDP-first for gameplay                           |
| Sync model               | Client prediction + server reconciliation        |
| Server simulation        | 60 Hz fixed timestep                             |
| Snapshot rate            | Lower than simulation rate, likely 20–30 Hz      |
| Simulation style         | Shared arcade car simulation                     |
| Determinism strategy     | Shared float simulation with tolerance tests     |
| Car configs              | Data-driven JSON                                 |
| Track configs            | JSON-authored track files                        |
| Lobby                    | Separate lobby service                           |
| Client ↔ lobby           | HTTP REST + JSON                                 |
| Lobby ↔ game server      | gRPC                                             |
| Client ↔ game server     | UDP MessagePack-style binary packets             |
| Message upgrade path     | Codec interface allows later custom binary codec |
| Player identity          | Nickname only                                    |
| Room security            | Short-lived signed join token                    |
| MVP room size            | 4 players                                        |
| Future room size target  | Design for 8 later                               |
| Deployment MVP           | Existing Linux machine                           |
| Runtime                  | Docker Compose                                   |
| Exposure path            | LAN/VPN first, public port forwarding later      |
| Later deployment path    | Kubernetes-ready, not MVP blocker                |
| Repo strategy            | Multiple public repos from day one               |
| License                  | MIT                                              |
| Shared code distribution | NuGet packages via GitHub Packages               |
| Package release flow     | Prerelease from `main`, stable from tags         |

---

## 4. Repository split

### Repos

```text
car-game-planning
car-game-client-unity
car-game-lobby-service
car-game-server-dotnet
car-game-protocol
car-game-shared-simulation
car-game-deploy
```

### Repo responsibilities

#### `car-game-planning`

Owns the planning source of truth.

Contains:

```text
PROJECT_SPEC.md
PROJECT_SPEC_TEMPLATE.md
PRODUCT_RULES.md
.ai-assembly/
planning_runs/
generated/
docs/
prompts/
verification/
```

Responsibilities:

* store project intake
* store planning runs
* store accepted specs
* store role prompts
* store backlog
* store verification rules
* document open questions and decisions

---

#### `car-game-client-unity`

Owns the Unity Windows client.

Responsibilities:

* main menu
* nickname entry
* room list/create/join UI
* car selection UI
* ready-up UI
* race HUD
* results screen
* UDP game connection
* input capture
* local prediction
* reconciliation smoothing
* track rendering from JSON
* car rendering from shared config
* importing protocol/simulation packages
* Windows build pipeline

Does **not** own:

* authoritative movement
* official race state
* official checkpoint/lap validation
* room assignment authority
* package definitions

---

#### `car-game-lobby-service`

Owns lobby discovery and room assignment.

Responsibilities:

* HTTP REST + JSON API for Unity client
* room list
* create room
* join room
* nickname acceptance
* short-lived join token issuing
* in-memory room state
* game-server registry
* game-server heartbeat handling
* gRPC control contract consumption
* basic lobby logs/health checks

Does **not** own:

* real-time car simulation
* UDP player input stream
* authoritative race physics
* long-term persistence

---

#### `car-game-server-dotnet`

Owns authoritative gameplay.

Responsibilities:

* UDP listener
* client handshake
* join token validation
* player session management
* room runtime
* 60 Hz simulation tick
* lower-rate snapshot sending
* authoritative car movement
* authoritative collision/checkpoint/lap state
* ready/countdown/race/results state machine
* gRPC registration/heartbeat with lobby
* Docker image for game server

Does **not** own:

* public room browsing UI
* account management
* persistent storage
* visual rendering

---

#### `car-game-protocol`

Owns shared protocol contracts.

Responsibilities:

* gameplay UDP message models
* message IDs
* protocol versioning
* packet envelope model
* sequence/ack fields
* MessagePack codec implementation
* codec interface
* golden packet tests
* gRPC `.proto` contracts for lobby ↔ game server
* REST DTOs if shared with lobby/client tooling
* NuGet package publishing

Important design rule:

```text
Game/client/server code must depend on protocol abstractions,
not directly on a specific serializer.
```

---

#### `car-game-shared-simulation`

Owns shared deterministic-ish arcade simulation.

Responsibilities:

* car state model
* player input model used by simulation
* fixed timestep simulation step
* acceleration/braking model
* steering model
* drift/grip/drag model
* collision primitives
* checkpoint/lap helpers if appropriate
* JSON car config schema/models
* JSON track config schema/models
* validation for configs
* tolerance tests
* NuGet package publishing

Important design rule:

```text
Unity physics must not be the source of truth for authoritative movement.
```

---

#### `car-game-deploy`

Owns deployment and operations.

Responsibilities:

* Docker Compose setup
* Linux server deployment docs
* environment variable templates
* firewall/port documentation
* LAN/VPN test instructions
* public port forwarding instructions
* logs/restart policy
* Kubernetes manifests for later
* basic smoke-test scripts

MVP runtime target:

```text
Docker Compose on existing Linux machine.
```

---

## 5. Package strategy

### Shared packages

```text
CarGame.Protocol
CarGame.SharedSimulation
```

### Targets

Both shared packages should multi-target:

```text
Unity-compatible target
.NET 10 target
```

The server consumes the .NET target.

The Unity client consumes Unity-compatible DLL/package artifacts.

### Publishing flow

Merge to `main`:

```text
run tests
build packages
publish prerelease package
example: 0.1.0-alpha.42
```

Version tag:

```text
run tests
build packages
publish stable package
example: 0.1.0
```

### Package rules

* no package publish if tests fail
* no breaking packet/config change without version note
* protocol and simulation packages require golden tests
* downstream repos pin package versions explicitly
* agents must document which package versions they tested against

---

## 6. Networking model

### Client ↔ lobby

Protocol:

```text
HTTP REST + JSON
```

Initial endpoints:

```text
GET  /health
GET  /rooms
POST /rooms
POST /rooms/{roomId}/join
POST /rooms/{roomId}/leave
```

The lobby returns:

```text
roomId
playerId
udpHost
udpPort
joinToken
tokenExpiresAt
```

---

### Lobby ↔ game server

Protocol:

```text
gRPC
```

Initial operations:

```text
RegisterGameServer
HeartbeatGameServer
CreateRoom
CloseRoom
GetServerStatus
```

Game server heartbeat includes:

```text
serverId
host
udpPort
activeRooms
maxRooms
activePlayers
maxPlayers
health
version
```

---

### Client ↔ game server

Protocol:

```text
UDP MessagePack-style binary packets
```

Packet envelope should include:

```text
protocolVersion
messageType
sequenceNumber
ackNumber
roomId
playerId/sessionId
payload
```

Core messages:

```text
ClientHello
ServerHello
JoinRoomHandshake
JoinRoomAccepted
JoinRoomRejected
PlayerInput
InputAck
ServerSnapshot
RaceStateChanged
Ping
Pong
Disconnect
Error
```

---

## 7. Simulation model

### Tick model

```text
Server simulation tick: 60 Hz
Snapshot send rate: 20–30 Hz initial target
Client render rate: Unity frame rate
Client prediction: local input tick
Reconciliation: against authoritative snapshots
```

### Authority rule

The server is the source of truth for:

* player position
* velocity
* heading
* collisions
* checkpoint order
* lap count
* finish time
* race result

The client may predict, interpolate, and smooth, but it must eventually obey the server.

### Car configs

Cars are defined in JSON.

Example shape:

```json
{
  "id": "rally_v1",
  "displayName": "Rally Car",
  "maxSpeed": 42.0,
  "accelerationCurve": [
    { "speed": 0.0, "acceleration": 18.0 },
    { "speed": 20.0, "acceleration": 12.0 },
    { "speed": 35.0, "acceleration": 5.0 }
  ],
  "brakeForce": 24.0,
  "turnRate": 3.8,
  "grip": 0.82,
  "driftFactor": 0.25,
  "drag": 0.08,
  "collisionRadius": 0.55
}
```

MVP car set:

```text
balanced_v1
speed_v1
grip_v1
```

### Track configs

Tracks are JSON-authored and consumed by both Unity and server.

MVP track contains:

```text
track ID
display name
spawn points
walls/collision segments
checkpoints
finish line
lap count
reset zones
optional visual hints
```

---

## 8. Security and safety boundaries

### MVP security

MVP includes:

* no accounts
* nickname only
* signed short-lived join tokens
* token checked during UDP handshake
* server rejects unknown/expired/invalid tokens
* server validates room/player assignment
* rate limiting or basic spam protection where practical
* no secrets committed to repos

### Out of scope for MVP

* full authentication
* persistent identity
* anti-cheat system
* payment systems
* public matchmaking moderation
* analytics tracking
* invasive telemetry

### Hard rule

Secrets must only live in:

```text
GitHub Actions secrets
local environment variables
server environment variables
ignored .env files
```

Never in public repos.

---

## 9. Agent roles

### 1. Planning Coordinator Agent

Owns:

* project spec
* repo plan
* backlog structure
* acceptance criteria
* cross-repo dependency ordering
* decision log
* open questions

Proof required:

* updated planning docs
* changed decisions clearly marked
* no silent scope expansion

---

### 2. Protocol Agent

Owns:

* `car-game-protocol`
* UDP packet models
* codec interface
* MessagePack codec
* message IDs
* gRPC proto contracts
* golden packet tests

Proof required:

* packet roundtrip tests
* unknown message handling tests
* version mismatch tests
* sample encoded fixtures
* published prerelease package

---

### 3. Shared Simulation Agent

Owns:

* `car-game-shared-simulation`
* fixed-step car movement
* car config models
* track config models
* simulation tests
* tolerance tests

Proof required:

* acceleration tests
* braking tests
* steering tests
* drift/grip tests
* config validation tests
* track validation tests
* published prerelease package

---

### 4. Lobby Service Agent

Owns:

* `car-game-lobby-service`
* REST API
* join token issuing
* room list/create/join
* game server heartbeat registry
* gRPC client/server integration as needed

Proof required:

* API tests
* join token expiry tests
* invalid token tests
* heartbeat tests
* room assignment tests
* Docker image builds

---

### 5. Game Server Agent

Owns:

* `car-game-server-dotnet`
* UDP listener
* player sessions
* token validation
* room runtime
* race state machine
* authoritative simulation integration
* snapshot sending
* lobby heartbeat

Proof required:

* UDP handshake tests
* invalid token rejection
* simulation tick tests
* 1/2/4-player room tests
* race state transition tests
* Docker image builds

---

### 6. Unity Client Agent

Owns:

* `car-game-client-unity`
* Windows client
* lobby UI
* room flow
* UDP connection
* input capture
* prediction
* reconciliation smoothing
* track rendering
* race HUD/results

Proof required:

* manual test steps
* screenshots or short capture notes
* local server connection proof
* prediction/reconciliation debug overlay
* Windows build artifact

---

### 7. Deploy/Ops Agent

Owns:

* `car-game-deploy`
* Docker Compose
* Linux machine deployment
* LAN/VPN setup docs
* public port forwarding docs
* environment templates
* service restart/log docs
* later Kubernetes scaffold

Proof required:

* Docker Compose starts all services
* health checks pass
* documented ports
* documented firewall rules
* documented rollback/restart steps

---

### 8. QA / Verification Agent

Owns:

* cross-repo verification
* edge-case tracking
* manual test plans
* multiplayer test matrix
* regression checklists
* “done means done” enforcement

Proof required:

* test matrix updated
* edge cases documented
* logs/screenshots attached where relevant
* no undocumented behavior drift

---

## 10. Definition of done

A task is done only when:

```text
- code builds
- relevant automated tests exist where practical
- manual test steps are written
- screenshots/logs are provided for visible or networking behavior
- a short change summary is included
- edge cases are explicitly documented
- edge-case behavior must not drift silently from the spec
```

Additional rules:

* protocol changes require packet tests
* simulation changes require tolerance/behavior tests
* config schema changes require sample valid/invalid fixtures
* deployment changes require runnable command examples
* client-visible changes require screenshot or recorded manual notes
* networking changes require logs or packet-level proof

---

## 11. First backlog

### Milestone 0 — Planning and repo bootstrap

#### PLANNING-001 — Create planning repo structure

Repo: `car-game-planning`

Tasks:

* add project spec
* add decision log
* add repo list
* add MVP boundary
* add verification rules
* add prompt pack skeleton

Acceptance:

* planning repo can explain the project without relying on chat history

---

#### PLANNING-002 — Create cross-repo dependency map

Repo: `car-game-planning`

Tasks:

* define package dependency graph
* define service dependency graph
* define which repo blocks which other repo

Acceptance:

* agents can identify what they need before starting work

---

### Milestone 1 — Protocol and simulation foundations

#### PROTOCOL-001 — Define message IDs and packet envelope

Repo: `car-game-protocol`

Acceptance:

* message type enum exists
* packet envelope model exists
* protocol version field exists
* sequence/ack fields exist
* unknown message behavior documented

---

#### PROTOCOL-002 — Implement codec interface and MessagePack codec

Repo: `car-game-protocol`

Acceptance:

* codec interface exists
* MessagePack codec implementation exists
* roundtrip tests pass
* invalid payload tests pass

---

#### PROTOCOL-003 — Define gRPC control proto

Repo: `car-game-protocol`

Acceptance:

* register/heartbeat/create-room contracts defined
* generated code builds
* sample request/response fixtures exist

---

#### SIM-001 — Define car state/input/config models

Repo: `car-game-shared-simulation`

Acceptance:

* car state model exists
* player input model exists
* JSON config model exists
* config validation exists

---

#### SIM-002 — Implement fixed-step arcade car movement

Repo: `car-game-shared-simulation`

Acceptance:

* acceleration/braking works
* steering works
* drag/grip works
* tests cover basic movement
* edge cases documented

---

#### SIM-003 — Define track JSON schema/model

Repo: `car-game-shared-simulation`

Acceptance:

* track model exists
* spawn/checkpoint/wall models exist
* validation catches invalid checkpoint order
* sample MVP track exists

---

### Milestone 2 — Lobby and game server skeleton

#### LOBBY-001 — Create lobby service skeleton

Repo: `car-game-lobby-service`

Acceptance:

* service starts
* `/health` works
* Dockerfile builds
* config via environment variables

---

#### LOBBY-002 — Implement room list/create/join API

Repo: `car-game-lobby-service`

Acceptance:

* rooms can be listed
* room can be created
* player can join room with nickname
* join response returns placeholder endpoint/token structure

---

#### LOBBY-003 — Implement short-lived join tokens

Repo: `car-game-lobby-service`

Acceptance:

* token issued on join
* token contains room/player expiry data
* invalid/expired token tests exist
* token secret not committed

---

#### SERVER-001 — Create game server skeleton

Repo: `car-game-server-dotnet`

Acceptance:

* service starts
* UDP socket binds
* Dockerfile builds
* health/log output exists

---

#### SERVER-002 — Implement UDP handshake with token validation

Repo: `car-game-server-dotnet`

Acceptance:

* valid token accepted
* expired token rejected
* wrong room rejected
* unknown player rejected
* handshake logs available

---

#### SERVER-003 — Implement lobby heartbeat via gRPC

Repo: `car-game-server-dotnet`

Acceptance:

* server registers with lobby
* heartbeat sends capacity/status
* lobby records server alive/dead state

---

### Milestone 3 — First playable network loop

#### SERVER-004 — Implement room runtime and 60 Hz simulation loop

Repo: `car-game-server-dotnet`

Acceptance:

* room ticks at fixed 60 Hz
* players have authoritative car states
* simulation package integrated
* server can run 1/2/4-player room tests

---

#### SERVER-005 — Implement input receive and snapshot send

Repo: `car-game-server-dotnet`

Acceptance:

* input packets accepted
* sequence numbers tracked
* snapshots sent at lower rate
* packet loss/reorder edge cases documented

---

#### CLIENT-001 — Create Unity project skeleton

Repo: `car-game-client-unity`

Acceptance:

* Unity project opens
* Windows build target configured
* package import process documented
* basic menu scene exists

---

#### CLIENT-002 — Implement lobby UI flow

Repo: `car-game-client-unity`

Acceptance:

* nickname entry
* list rooms
* create room
* join room
* receive UDP endpoint/token

---

#### CLIENT-003 — Implement UDP client handshake

Repo: `car-game-client-unity`

Acceptance:

* sends join token to server
* handles accepted/rejected response
* logs connection state

---

#### CLIENT-004 — Implement local input and prediction

Repo: `car-game-client-unity`

Acceptance:

* player car responds immediately to input
* input sequence numbers generated
* local simulation uses shared package

---

#### CLIENT-005 — Implement snapshot reconciliation

Repo: `car-game-client-unity`

Acceptance:

* authoritative snapshot applied
* local prediction corrected smoothly
* debug display shows correction amount

---

### Milestone 4 — Race MVP loop

#### SERVER-006 — Implement ready/countdown/race/results state machine

Repo: `car-game-server-dotnet`

Acceptance:

* players can ready up
* countdown starts
* race starts
* finish detected
* results generated

---

#### SIM-004 — Implement checkpoint/lap validation helpers

Repo: `car-game-shared-simulation`

Acceptance:

* checkpoint order validated
* lap completion detected
* missed checkpoint edge cases documented

---

#### CLIENT-006 — Implement race HUD and ready/results screens

Repo: `car-game-client-unity`

Acceptance:

* ready button
* countdown display
* lap/checkpoint display
* finish results screen

---

#### CLIENT-007 — Render JSON track and cars

Repo: `car-game-client-unity`

Acceptance:

* MVP track loads from JSON
* spawn points applied
* checkpoint/wall visuals visible
* cars rendered with distinct visual placeholders

---

### Milestone 5 — Deployment and first server test

#### DEPLOY-001 — Docker Compose for Linux machine

Repo: `car-game-deploy`

Acceptance:

* lobby service starts
* game server starts
* environment variables documented
* logs visible
* restart policy defined

---

#### DEPLOY-002 — LAN/VPN test instructions

Repo: `car-game-deploy`

Acceptance:

* Linux server setup documented
* client connection instructions documented
* firewall requirements documented
* known failure modes documented

---

#### DEPLOY-003 — Public port forwarding guide

Repo: `car-game-deploy`

Acceptance:

* lobby TCP port documented
* game UDP port documented
* router/firewall checklist documented
* CGNAT caveat documented
* cheap VPS fallback noted

---

#### QA-001 — End-to-end MVP test plan

Repo: `car-game-planning` or `car-game-deploy`

Acceptance:

* 1-player smoke test
* 2-player test
* 4-player test
* reconnect/invalid-token tests
* race completion test
* Linux deployment test

---

## 12. Key edge cases to document from day one

### Networking

* duplicate UDP packets
* out-of-order input packets
* missing snapshots
* player disconnect during countdown
* player disconnect during race
* invalid join token
* expired join token
* token for wrong room
* same nickname collision
* room full
* game server heartbeat lost
* lobby restarts while game server still runs
* client joins room after race already started

### Simulation

* car starts inside wall
* checkpoint crossed backwards
* checkpoint skipped
* car leaves track
* zero throttle/brake conflict
* extreme steering values
* invalid car config
* invalid track config
* low FPS client prediction
* server tick jitter

### Deployment

* UDP port blocked
* HTTP port blocked
* Docker service restart
* Linux firewall missing rule
* router port forwarding wrong target
* CGNAT prevents public hosting
* server local IP changes
* join token secret missing

---

## 13. Verification rules

### General

Every repo must have:

* README
* setup instructions
* build/test command
* license
* contribution notes
* edge-case section
* current package/service version notes where relevant

### Protocol repo

Must verify:

* packet roundtrip
* malformed packet rejection
* protocol version mismatch
* message ID stability
* codec abstraction preserved
* golden packet fixtures

### Shared simulation repo

Must verify:

* fixed timestep behavior
* car acceleration curves
* braking behavior
* steering behavior
* drift/grip behavior
* config validation
* track validation
* tolerance expectations

### Lobby repo

Must verify:

* room creation
* room listing
* room join
* room full rejection
* token issuing
* token expiry
* game server heartbeat handling

### Server repo

Must verify:

* UDP bind/start
* handshake
* token validation
* input processing
* snapshot sending
* race state machine
* 1/2/4-player rooms

### Client repo

Must verify:

* Windows build
* lobby connection
* room join
* UDP handshake
* local prediction
* reconciliation
* HUD/results
* manual screenshots/logs

### Deploy repo

Must verify:

* Docker Compose starts
* service logs visible
* ports documented
* LAN/VPN instructions tested
* public port forwarding instructions documented
* Kubernetes path scaffolded but not required

---

## 14. Prompt pack outline

### `00-planning-coordinator.md`

Role:

You maintain the source-of-truth planning state. Keep scope controlled, update decisions, prevent silent drift, and split work into small verifiable tasks.

---

### `01-protocol-agent.md`

Role:

You own wire contracts. Build the UDP packet model, codec abstraction, MessagePack implementation, gRPC proto contracts, and golden protocol tests.

---

### `02-shared-simulation-agent.md`

Role:

You own the shared arcade simulation. Implement fixed-step car physics, JSON car configs, JSON track configs, and tolerance-tested behavior.

---

### `03-lobby-service-agent.md`

Role:

You own the lobby service. Implement REST room APIs, join-token issuing, in-memory room state, and heartbeat-based game-server registry.

---

### `04-game-server-agent.md`

Role:

You own the authoritative game server. Implement UDP handshake, token validation, room runtime, simulation loop, snapshots, race state, and lobby gRPC heartbeat.

---

### `05-unity-client-agent.md`

Role:

You own the Unity desktop client. Implement menu flow, room join, UDP connection, local prediction, reconciliation, rendering, HUD, and Windows build.

---

### `06-deploy-ops-agent.md`

Role:

You own Linux deployment. Provide Docker Compose, server setup docs, LAN/VPN testing, port forwarding docs, logs, restart behavior, and later Kubernetes scaffold.

---

### `07-qa-verification-agent.md`

Role:

You enforce done-ness. Maintain edge-case lists, test matrices, manual test plans, regression checks, and proof requirements across all repos.

---

## 15. Open questions

These are not blockers for planning, but should be resolved before or during early implementation.

1. Exact Unity version.
2. Exact Unity-compatible target for shared packages.
3. Exact package naming convention under GitHub Packages.
4. Whether package publishing uses repository-level or organization-level package namespace.
5. Which MessagePack library to use.
6. Exact gRPC tooling approach for `.proto` generation.
7. Exact Linux server environment.
8. Whether the Linux server has public IPv4 or CGNAT.
9. Initial UDP and HTTP port numbers.
10. First track theme/name.
11. First 3 car names and tuning profiles.
12. Whether collisions between cars are enabled in MVP or only wall/checkpoint collision.
13. Whether rooms allow late join before countdown only or during race as spectator/not allowed.
14. Whether race lap count is 1, 2, or 3 for MVP.

---

## 16. Recommended first execution order

Do **not** start with Unity visuals first.

Start with contracts and simulation:

```text
1. car-game-planning
2. car-game-protocol
3. car-game-shared-simulation
4. car-game-lobby-service skeleton
5. car-game-server-dotnet skeleton
6. car-game-deploy Docker Compose
7. car-game-client-unity skeleton
8. end-to-end handshake
9. input/snapshot loop
10. prediction/reconciliation
11. race state
12. Windows MVP build
13. Linux server test
```

Reason:

The hardest risk is not drawing cars. The hardest risk is making a multi-repo, UDP, prediction-based client/server architecture stay coherent. Get the contracts and simulation stable first, then visuals become much safer.

---

## 17. MVP acceptance test

The MVP is accepted when:

```text
Given the Linux server is running Docker Compose,
and 2–4 Windows clients launch the Unity build,
and each player enters a nickname,
and each player joins the same room,
and each player selects a car,
and all players ready up,
then the server starts a countdown,
then all players race on the same JSON-defined track,
then checkpoint/lap progress is authoritative,
then finish results are shown to all clients,
and the server logs the race completion,
and all documented MVP edge cases have explicit expected behavior.
```
