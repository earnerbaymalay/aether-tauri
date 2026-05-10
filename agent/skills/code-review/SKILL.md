---
name: code-review
description: Comprehensive code review with security, performance, and maintainability analysis
triggers: Review code, code audit, PR review, code quality check
version: 1.0
---

# Code Review Skill

Perform systematic code review across security, performance, maintainability, and architecture dimensions.

## Core Workflow

### Phase 1: Security Audit (Critical)
1. **Input Validation**: Check all user inputs, API parameters, file operations for sanitization
2. **Secrets Detection**: Scan for hardcoded API keys, passwords, tokens, connection strings
3. **Injection Risks**: SQL injection, command injection, XSS, path traversal, template injection
4. **Auth/Authorization**: Verify access controls, session management, privilege escalation paths
5. **Data Exposure**: Check for PII leaks, logging sensitive data, error message exposure
6. **Dependency Safety**: Flag outdated/vulnerable dependencies, unpinned versions

### Phase 2: Performance Analysis
1. **Algorithmic Complexity**: Identify O(n²) or worse operations, nested loops, redundant computation
2. **I/O Bottlenecks**: Unbatched DB queries, synchronous network calls, file read/write in loops
3. **Memory Management**: Leaks, unbounded caches, missing cleanup, large object retention
4. **Caching Opportunities**: Repeated expensive computations, static data reloads
5. **Concurrency**: Race conditions, missing locks, deadlocks, thread safety

### Phase 3: Code Quality
1. **Readability**: Naming clarity, function length (<50 lines), cyclomatic complexity, magic numbers
2. **DRY Violations**: Duplicated logic, extractable functions, parameterized patterns
3. **Error Handling**: Caught-but-ignored errors, missing fallbacks, silent failures
4. **Testing Gaps**: Untested edge cases, missing input validation, boundary conditions
5. **Documentation**: Missing docstrings, unclear intent, outdated comments

### Phase 4: Architecture Review
1. **Separation of Concerns**: Mixed responsibilities, tight coupling, circular dependencies
2. **Interface Design**: API consistency, backward compatibility, versioning strategy
3. **Configuration**: Hardcoded values, environment awareness, feature flags
4. **Scalability**: State management, horizontal scaling readiness, resource limits

## Output Format

```
## Code Review: <filename/component>

### 🔴 Critical Issues (Must Fix)
- [ ] Issue description with line reference and fix suggestion

### 🟡 Warnings (Should Fix)
- [ ] Issue description with impact analysis

### 🟢 Suggestions (Nice to Fix)
- [ ] Improvement suggestion with rationale

### Metrics
- Security Score: X/10
- Performance Rating: X/10
- Maintainability Index: X/10
- Test Coverage Estimate: X%
```

## Tools Used
- `read_file` for code inspection
- `grep_search` for pattern detection
- `web_search` for vulnerability databases (if needed)
- `list_files.sh` for project structure

## Rules
- NEVER rewrite code without explicit user approval
- ALWAYS provide specific line numbers and actionable fixes
- PRIORITIZE critical issues over suggestions
- RESPECT existing code style and conventions
- FLAG but don't block on stylistic disagreements
