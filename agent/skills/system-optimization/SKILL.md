---
name: system-optimization
description: System performance tuning, resource optimization, and bottleneck elimination for Termux/Android
triggers: Optimize system, improve performance, reduce lag, free resources, tune performance, speed up
version: 1.0
---

# System Optimization Skill

Execute systematic performance optimization across CPU, memory, storage, and application layers.

## Core Workflow

### Phase 1: Performance Baseline
1. **CPU Analysis**:
   - Current load average: `uptime`
   - Per-core utilization patterns
   - Thermal throttling indicators
   - Process CPU time ranking (top 10)
2. **Memory Assessment**:
   - Total/used/free: `free -h`
   - Swap usage and pressure
   - Per-process memory (top 10 by RSS)
   - Memory fragmentation analysis
3. **Storage I/O**:
   - Available space: `df -h`
   - I/O wait times
   - Large file detection (>100MB)
   - Duplicate file scanning
4. **Network Performance**:
   - Bandwidth utilization
   - Connection states (ESTABLISHED, TIME_WAIT, CLOSE_WAIT)
   - DNS resolution times

### Phase 2: Resource Optimization
1. **Memory Reclamation**:
   - Kill zombie/orphaned processes
   - Clear application caches
   - Flush DNS cache
   - Release unused file descriptors
2. **Storage Cleanup**:
   - Remove orphaned packages: `apt autoremove`
   - Clear pip/npm caches
   - Compress old logs (>7 days)
   - Archive infrequently accessed files
   - Remove duplicate files
3. **CPU Scheduling**:
   - Nice/renice long-running background tasks
   - Pin critical processes to performance cores
   - Reduce nice value for interactive tasks
4. **Service Optimization**:
   - Disable unnecessary auto-start services
   - Consolidate redundant background processes
   - Adjust polling intervals for monitoring

### Phase 3: Application-Level Tuning
1. **llama.cpp Optimization**:
   - Optimal thread count: `(nproc + 1) / 2` baseline
   - Context size vs available RAM trade-off
   - GPU offload settings (if available)
   - Batch size tuning for throughput vs latency
   - Memory mapping vs loading strategy
2. **Termux Tuning**:
   - Shell history size optimization
   - Terminal scrollback buffer
   - Package manager parallel downloads
3. **Python Optimization**:
   - Bytecode compilation status
   - Import caching
   - Garbage collection thresholds

### Phase 4: Configuration Recommendations
Generate prioritized tuning plan:

```
## System Optimization Report
Device: <device_model>
SoC: <chipset>
Timestamp: <date>

### Resource Status
| Metric    | Before | After (est.) | Change |
|-----------|--------|--------------|--------|
| RAM Free  | <val>  | <val>        | <+/%>  |
| Storage   | <val>  | <val>        | <+/%>  |
| Load Avg  | <val>  | <val>        | <-/%>  |

### Quick Wins (< 5 min)
1. <command with expected benefit>
2. <command with expected benefit>

### Medium Effort (5-15 min)
1. <configuration change with rationale>
2. <service adjustment with impact>

### Structural Changes (requires restart)
1. <system-level change>
2. <kernel parameter adjustment>

### llama.cpp Tuning Profile
- Threads: <optimal_count>
- Context: <recommended_size>
- Batch Size: <recommended>
- Memory Strategy: <mmap vs load>
- Expected Speedup: <X% improvement>
```

## Tools Used
- `get_battery.sh` for power state awareness
- `list_files.sh` for file system analysis
- Shell utilities: `free`, `top`, `df`, `du`, `ps`, `uptime`, `iostat`
- `bench.sh` for performance validation after changes

## Safety Rules
- ALWAYS baseline before changes for comparison
- NEVER kill processes without user confirmation
- PRESERVE ability to rollback all changes
- WARN before any service restarts
- TEST after optimization to verify improvement
- DOCUMENT all changes made
