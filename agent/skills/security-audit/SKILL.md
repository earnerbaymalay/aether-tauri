---
name: security-audit
description: Multi-layer security scanning with nmap, process audit, network analysis, and vulnerability assessment
triggers: Security scan, vulnerability check, system hardening, penetration test, audit system
version: 1.0
---

# Security Audit Skill

Execute comprehensive security audit across network, process, file, and configuration layers.

## Core Workflow

### Phase 1: Network Reconnaissance
1. **Port Scan**: Use `nmap -sV -sC -O <target>` for service version detection
2. **Vulnerability Scan**: `nmap --script vuln <target>` for known CVEs
3. **Network Map**: `nmap -sn <subnet>` for host discovery
4. **Service Fingerprinting**: Identify running services and versions
5. **Firewall Check**: Verify closed ports, default deny policy

### Phase 2: Process Security Audit
1. **Running Processes**: `ps aux` with privilege analysis
   - Flag processes running as root unnecessarily
   - Identify world-writable executables
   - Check for known vulnerable software versions
2. **Permission Audit**: 
   - SUID/SGID binaries: `find / -perm /6000 2>/dev/null`
   - World-writable directories: `find / -type d -perm -o+w 2>/dev/null`
   - Open SSH keys: `find ~ -name "*.pem" -o -name "id_*" | xargs ls -la`
3. **Environment Security**:
   - Exposed variables: `env | grep -iE "key|pass|token|secret"`
   - PATH injection risks: `echo $PATH | tr ':' '\n' | xargs -I{} ls -ld {}`

### Phase 3: File System Security
1. **Sensitive File Exposure**:
   - Check `~/.bash_history` for leaked credentials
   - Audit `~/.ssh/` permissions (should be 700 for dir, 600 for keys)
   - Verify `.env` files are in `.gitignore`
2. **Log Analysis**:
   - Check `~/.audit_logs/` for previous findings
   - Scan for failed login attempts
   - Review sudo usage patterns
3. **Backup Security**:
   - Verify backup encryption status
   - Check backup file permissions
   - Ensure backup locations are secure

### Phase 4: Application Security
1. **API Endpoint Audit**:
   - Test authentication requirements
   - Check for CORS misconfigurations
   - Verify rate limiting is enabled
2. **Configuration Review**:
   - Flag `allow_origins=["*"]` patterns
   - Check debug mode is disabled in production
   - Verify TLS/SSL configuration
3. **Dependency Check**:
   - `npm audit` for Node.js projects
   - `pip list --outdated` for Python
   - Check for known vulnerable llama.cpp versions

### Phase 5: Hardening Recommendations
Generate prioritized action list:

```
## Security Audit Report
Timestamp: <date>
Target: <system/network>

### 🔴 Critical Vulnerabilities
- [ ] Description with CVE reference (if applicable)
  - Risk: <impact description>
  - Fix: <specific command/steps>

### 🟡 High-Risk Findings
- [ ] Description with exploitation path
  - Risk: <impact>
  - Fix: <steps>

### 🟢 Hardening Opportunities
- [ ] Improvement with security benefit
  - Implementation: <commands>

### Network Summary
- Open Ports: <list>
- Vulnerable Services: <count>
- Failed Auth Attempts: <count>

### System Summary
- SUID Binaries: <count>
- Exposed Secrets: <count>
- Permission Issues: <count>
```

## Tools Used
- `vault-scan.sh` for baseline security scan
- `nmap` for network reconnaissance
- `get_battery.sh` for system status during scan
- `list_files.sh` for file system audit
- `web_search.sh` for CVE lookups

## Safety Rules
- NEVER run destructive scans on production without explicit confirmation
- ALWAYS limit scan scope to authorized targets
- LOG all findings to `~/.audit_logs/security_audit_<timestamp>.log`
- WARN before suggesting any service restarts or config changes
- RESPECT air-gapped environments (skip network scans if offline)
