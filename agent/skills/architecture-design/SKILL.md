---
name: architecture-design
description: System architecture design, component modeling, and technical decision analysis for software projects
triggers: Design architecture, system design, technical planning, component design, refactor architecture, technical decision
version: 1.0
---

# Architecture Design Skill

Guide systematic architecture design from requirements through implementation roadmap with trade-off analysis.

## Core Workflow

### Phase 1: Requirements Decomposition
1. **Functional Requirements**:
   - Core user stories and use cases
   - Input/output contracts
   - State management needs
   - Integration points
2. **Non-Functional Requirements**:
   - Performance targets (latency, throughput)
   - Scalability expectations (users, data volume)
   - Availability requirements (uptime SLA)
   - Security constraints (data sensitivity, compliance)
3. **Constraints Identification**:
   - Platform limitations (Android/Termux, resource caps)
   - Technology stack requirements
   - Timeline and team capacity
   - Budget/resource constraints

### Phase 2: Architectural Pattern Selection
Evaluate patterns against requirements:

1. **Layered Architecture**:
   - Best for: Clear separation of concerns, testability
   - Trade-off: Can introduce latency through layers
   
2. **Event-Driven Architecture**:
   - Best for: Asynchronous processing, loose coupling
   - Trade-off: Complexity in event ordering, debugging

3. **Microservices/Modular Monolith**:
   - Best for: Independent scaling, team autonomy
   - Trade-off: Network overhead, deployment complexity

4. **Pipeline/Filter Pattern**:
   - Best for: Data transformation, processing chains
   - Trade-off: Rigid flow, harder to branch

5. **Plugin/Extension Architecture**:
   - Best for: Extensibility, third-party integrations
   - Trade-off: API stability, version management

### Phase 3: Component Design
1. **Component Identification**:
   - Core domain logic
   - Data access layer
   - Presentation/interface layer
   - Infrastructure services
2. **Interface Definition**:
   - Public APIs per component
   - Data contracts (schemas, types)
   - Event contracts (if event-driven)
   - Error handling contracts
3. **Dependency Mapping**:
   - Component dependency graph
   - Circular dependency detection
   - External dependency inventory
   - Version compatibility matrix

### Phase 4: Technology Decision Matrix
For each technology choice, evaluate:

```
| Criterion          | Weight | Option A | Option B | Option C |
|--------------------|--------|----------|----------|----------|
| Performance        | 0.25   | score    | score    | score    |
| Development Speed  | 0.20   | score    | score    | score    |
| Maintenance Cost   | 0.15   | score    | score    | score    |
| Team Familiarity   | 0.15   | score    | score    | score    |
| Ecosystem Maturity | 0.10   | score    | score    | score    |
| Platform Fit       | 0.15   | score    | score    | score    |
| WEIGHTED TOTAL     | 1.00   | total    | total    | total    |
```

### Phase 5: Architecture Documentation
Generate architecture decision record:

```
## Architecture Design: <system_name>

### Context
<problem statement and requirements summary>

### Decision
<chosen architecture pattern and rationale>

### Component Diagram
<text-based component layout with relationships>

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Presentation  │────>│    Business     │────>│    Data         │
│   Layer         │     │    Logic        │     │    Access       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Technology Stack
| Layer | Technology | Justification | Alternatives Considered |
|-------|-----------|---------------|------------------------|
| <layer> | <tech> | <why> | <alternatives> |

### Key Decisions
1. **<Decision>**: <rationale and trade-offs>
2. **<Decision>**: <rationale and trade-offs>

### Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| <risk> | <H/M/L> | <H/M/L> | <strategy> |

### Migration Path (if refactoring)
Phase 1: <initial steps>
Phase 2: <transition steps>
Phase 3: <completion steps>
```

## Tools Used
- `list_files.sh` for current codebase exploration
- `read_file` for existing architecture review
- `grep_search` for pattern detection in current code
- `web_read.sh` for architecture pattern research
- `web_search.sh` for technology comparisons

## Design Principles
- FAVOR simplicity over cleverness
- PREFER composition over inheritance
- DESIGN for failure (graceful degradation)
- PLAN for change (abstraction at volatility points)
- OPTIMIZE for developer experience
- DOCUMENT decisions and rationale (not just what, but WHY)
- VALIDATE against real constraints (not hypothetical scale)
