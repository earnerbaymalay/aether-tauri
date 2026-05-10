---
name: project-planning
description: Project planning, task breakdown, milestone tracking, and sprint management for software development
triggers: Plan project, break down tasks, create roadmap, sprint planning, project management, estimate work
version: 1.0
---

# Project Planning Skill

Guide systematic project planning from vision through executable task breakdown with realistic estimation.

## Core Workflow

### Phase 1: Vision & Scope Definition
1. **Problem Statement**:
   - What problem are we solving?
   - Who is the target user?
   - What does success look like?
   - What are the acceptance criteria?
2. **Scope Boundaries**:
   - IN scope: explicit feature list
   - OUT of scope: explicit exclusions
   - Future considerations (backlog items)
3. **Success Metrics**:
   - Quantitative measures (performance targets, user counts)
   - Qualitative measures (user satisfaction, code quality)
   - Milestone checkpoints

### Phase 2: Task Decomposition
Break work into hierarchical structure:

```
Epic: <major capability>
├── Feature: <specific capability>
│   ├── Story: <user-facing deliverable>
│   │   ├── Task: <implementable unit, 2-8 hours>
│   │   ├── Task: <implementable unit>
│   │   └── Task: <implementable unit>
│   └── Story: <user-facing deliverable>
│       └── ...
└── Feature: <specific capability>
    └── ...
```

### Phase 3: Dependency Mapping
1. **Technical Dependencies**:
   - Prerequisite components
   - Parallelizable work streams
   - Integration points requiring coordination
2. **External Dependencies**:
   - Third-party APIs/libraries
   - Infrastructure requirements
   - Team member availability
3. **Critical Path Analysis**:
   - Identify longest dependency chain
   - Flag bottleneck tasks
   - Suggest parallelization opportunities

### Phase 4: Effort Estimation
Use three-point estimation for each task:
- **Optimistic (O)**: Everything goes perfectly
- **Realistic (R)**: Normal conditions
- **Pessimistic (P)**: Everything that can go wrong does

**Expected Effort** = (O + 4R + P) / 6

Group into T-shirt sizes:
- XS: < 1 hour
- S: 1-4 hours
- M: 4-8 hours (1 day)
- L: 1-3 days
- XL: 3-5 days (break down further if possible)

### Phase 5: Milestone Planning
Define milestones as shippable increments:

```
Milestone 1: <name> - <date/iteration>
- Deliverable: <concrete output>
- Acceptance: <testable criteria>
- Dependencies: <what must be complete>

Milestone 2: <name> - <date/iteration>
...
```

### Phase 6: Risk Assessment
| Risk | Probability | Impact | Mitigation | Contingency |
|------|------------|--------|------------|-------------|
| <technical risk> | <H/M/L> | <H/M/L> | <prevention> | <fallback> |

## Output Format

```
## Project Plan: <project_name>

### Vision
<one-paragraph description of what we're building and why>

### Scope
**IN**: <key features>
**OUT**: <explicit exclusions>

### Architecture Overview
<brief technical approach>

### Task Breakdown
<hierarchical task list with estimates>

### Dependencies & Critical Path
<dependency graph analysis>

### Milestones
<shippable increments with criteria>

### Risk Register
<identified risks with mitigations>

### Resource Requirements
- <what's needed to execute>
```

## Tools Used
- `list_files.sh` for existing codebase analysis
- `read_file` for current state assessment
- `get_date.sh` for timeline anchoring
- `grep_search` for dependency discovery

## Planning Rules
- BREAK DOWN tasks to <1 day effort (if larger, decompose further)
- IDENTIFY at least 3 risks per project
- DEFINE concrete acceptance criteria per milestone
- FLAG unknowns explicitly (don't pretend certainty)
- INCLUDE integration and testing time (not just feature dev)
- VALIDATE estimates against historical data (if available)
- PLAN for 70% capacity (buffer for unexpected work)
