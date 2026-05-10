---
name: active-defense
description: Proactive hardware telemetry and security risk analysis
triggers: Security status, system health, check threats, monitor hardware
version: 1.0
---

# Active Defense Skill

Ported from Edge Sentinel, this skill enables Aether to monitor system hardware for security anomalies.

## Core Workflow

### Phase 1: Telemetry Acquisition
1. **Hardware State**:
   - Battery: Percentage, temperature, health, status.
   - CPU: Load averages, per-process utilization.
   - Memory: RSS vs Swap usage, fragmentation.
2. **Network Perimeter**:
   - Real-time Packet Inspection: High-volume exfiltration detection via `net_monitor.py`.
   - Active connections: `netstat -tunp`
   - Listening ports: `lsof -i -P -n`
   - Data flow patterns.

### Phase 2: AI Risk Analysis
1. **Anomaly Detection**: Identifying unusual battery drain or CPU spikes that might indicate crypto-jacking or background exfiltration.
2. **Deep Packet Analysis**: Using Scapy-powered heuristics to detect encrypted tunnels to non-standard ports.
3. **Sentiment Analysis of System Logs**: Searching for "fail," "denied," "unauthorized" in system logs.

### Phase 3: Defensive Action
1. **Alerting**: High-priority notifications for critical hardware states or suspicious network flows.
2. **Containment**: Recommendation to kill suspicious PIDs or block offending IPs.
3. **Hardening**: Automatic flush of DNS cache and closing of unneeded ports.

## Tools Used
- `system_monitor.ps1`
- `net_monitor.py` (Hardened)
- `net_recon.ps1`
- `log_analyzer.ps1`
- `system_optimizer.py`

## Rules
- NEVER ignore high battery temperatures.
- PRIORITIZE physical hardware health over process uptime.
- ALWAYS notify the user before taking a containment action.
