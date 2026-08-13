# 🛡️ Detection Engineering & Threat Hunting Lab (Wazuh + Sysmon + MITRE ATT&CK)

[![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)](#version-history--release-notes)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Rule Tests](https://img.shields.io/badge/Rule%20Tests-8%2F8%20passed-brightgreen.svg)](tests/logtest_samples.json)
[![SIEM](https://img.shields.io/badge/SIEM-Wazuh--4.7.2-green.svg)](https://wazuh.com)
[![Telemetry](https://img.shields.io/badge/Telemetry-Sysmon--v15-orange.svg)](configs/sysmonconfig-export.xml)
[![Framework](https://img.shields.io/badge/Framework-MITRE%20ATT%26CK-red.svg)](https://attack.mitre.org)

> A SOC detection engineering lab built to simulate real-world cyber attack techniques, capture endpoint telemetry via Sysmon, author custom Wazuh SIEM detection rules (parent correlation & standalone field matching), and perform structured incident response.

---

## 📸 Executive Dashboard & Telemetry Overview

![Wazuh Security Dashboard](screenshots/dashboard.png)
*Figure 1.1: Main Wazuh SIEM Security Events Overview Dashboard showing active agent monitoring and alert telemetry.*

---

## 🏗️ Architecture & Infrastructure Design

```mermaid
flowchart TD
    subgraph Host["Host Operating System (macOS / Linux)"]
        subgraph DockerCompose["Single-Node Docker Compose Deployment"]
            WI["Wazuh Indexer (OpenSearch)<br>Port: 9200"]
            WM["Wazuh Manager (v4.7.2)<br>Ports: 1514 (TCP/UDP), 1515 (TCP), 55000 (TCP)"]
            WD["Wazuh Dashboard (UI)<br>Port: 443 (HTTPS)"]
            WI <-->|Storage / Indexing| WM
            WM <-->|API / Log Pipeline| WD
        end
    end

    subgraph TargetVM["Target Virtual Machine (Windows 11 Pro)"]
        ART["Atomic Red Team<br>(Attack Execution Suite)"]
        SYS["Microsoft Sysmon<br>(Pinned Config: sysmonconfig-export.xml)"]
        WA["Wazuh Windows Agent (v4.7.2)<br>(EventChannel Log Forwarder)"]
        ART -->|Generates Telemetry| SYS
        SYS -->|Operational Logs| WA
    end

    WA == "Encrypted EventChannel Log Stream (Port 1514)" ==> WM
```

### Infrastructure Specs
- **SIEM Manager**: Wazuh Manager (Self-Hosted via Docker Compose Stack)
- **Log Search & Indexing**: Wazuh Indexer (OpenSearch)
- **Monitored Endpoint**: Windows 11 Pro Virtual Machine (VirtualBox NAT Network)
- **Telemetry Engine**: Microsoft Sysmon ([`configs/sysmonconfig-export.xml`](configs/sysmonconfig-export.xml))
- **Attack Automation**: Red Canary Atomic Red Team ([`configs/atomic_red_team_guide.md`](configs/atomic_red_team_guide.md))

---

## 🌐 Network & Agent Enrollment Requirements

### Required Network Ports
| Port | Protocol | Service / Direction | Description |
|---|---|---|---|
| **1514** | TCP / UDP | Endpoint $\rightarrow$ Manager | Encrypted EventChannel agent log stream |
| **1515** | TCP | Endpoint $\rightarrow$ Manager | Wazuh agent enrollment & registration service |
| **55000** | TCP | Dashboard $\rightarrow$ Manager | Wazuh Manager REST API communication |
| **443** | TCP | User $\rightarrow$ Dashboard | HTTPS Wazuh Dashboard Web Interface |

### Agent Enrollment & Configuration
1. **Enroll Agent via PowerShell (Admin)**:
   ```powershell
   & "C:\Program Files (x86)\ossec-agent\agent-auth.exe" -m <WAZUH_MANAGER_IP> -p 1515
   ```
2. **Configure `<client>` Block in `C:\Program Files (x86)\ossec-agent\ossec.conf`**:
   ```xml
   <ossec_config>
     <client>
       <server>
         <address><WAZUH_MANAGER_IP></address>
         <port>1514</port>
         <protocol>tcp</protocol>
       </server>
     </client>
   </ossec_config>
   ```
3. **Verify Enrollment**:
   ```powershell
   Restart-Service -Name Wazuh
   & "C:\Program Files (x86)\ossec-agent\wazuh-agent.exe" -status
   ```

---

## 📊 MITRE ATT&CK Detection Matrix

| # | Technique Name | MITRE ID | Tactic | Parent Rule | Custom Rule ID | Rule Engineering Type | Severity | Status |
|---|---|---|---|---|---|---|---|---|
| **1** | Base64 Encoded PowerShell | `T1059.001` | Execution | `92057` | **`100100`**<br>**`100105`** | Parent Correlation / Escalation<br>Standalone Sysmon Field Match | Level 15 (Critical) | ✅ Verified |
| **2** | Scheduled Task Creation | `T1053.005` | Persistence | `92032` | **`100101`** | Standalone Sysmon Field Match | Level 12 (High) | ✅ Verified |
| **3** | Registry Run Key Persistence | `T1547.001` | Persistence | `92302` | **`100102`** | Parent Correlation / Escalation | Level 12 (High) | ✅ Verified |
| **4** | Clear Windows Event Logs | `T1070.001` | Defense Evasion | Sysmon EID 1 | **`100103`** | Standalone Sysmon Field Match | Level 13 (High) | ✅ Verified |
| **5** | Credential Store Enumeration | `T1555.004` | Credential Access | Sysmon EID 1 | **`100104`** | Standalone Sysmon Field Match | Level 14 (High) | ✅ Verified |

---

## ⏱️ Lab Setup Time Estimates

| Phase | Task | Tools Required | Estimated Time |
|---|---|---|---|
| **Phase 1** | Install Docker & Docker Compose | Docker Desktop / CLI | 10 mins |
| **Phase 2** | Deploy Wazuh SIEM Stack | `docker compose -f docker/docker-compose.yml up -d` | 15 mins |
| **Phase 3** | Install Sysmon with Pinned Config | Sysinternals Sysmon + `sysmonconfig-export.xml` | 5 mins |
| **Phase 4** | Install & Register Wazuh Agent | Agent Auth + `ossec.conf` binding | 5 mins |
| **Phase 5** | Install Atomic Red Team & Execute Attacks | Invoke-AtomicRedTeam | 10 mins |
| **TOTAL** | **Complete Lab Deployment** | - | **~45 mins** |

---

## 🚀 Step-by-Step Deployment Guide

### 1. Deploy Wazuh SIEM Stack
```bash
git clone https://github.com/sanjaypramodprathibha/detection-engineering-lab.git
cd detection-engineering-lab/docker
docker compose up -d
```

### 2. Configure Sysmon & Agent on Windows 11 VM
1. Install Sysmon using pinned configuration:
   ```cmd
   sysmon64.exe -i configs/sysmonconfig-export.xml -accepteula
   ```
2. Paste the `<localfile>` block from [`configs/wazuh_agent_ossec_snippet.xml`](configs/wazuh_agent_ossec_snippet.xml) inside `C:\Program Files (x86)\ossec-agent\ossec.conf`.

### 3. Deploy Custom Rules
Paste [`custom_rules/local_rules.xml`](custom_rules/local_rules.xml) into `/var/ossec/etc/rules/local_rules.xml` on your Wazuh Manager:

![Wazuh Custom Rules Editor](screenshots/custom_rule.png)
*Figure 3.1: Custom rule engineering inside the Wazuh Web UI rule editor.*

### 4. Run Validation Suite
Execute the automated test suite locally:
```bash
python3 tests/run_tests.py
```

---

## 🛠️ Custom Rule Engineering (Correlation vs Standalone)

1. **Parent Correlation & Severity Escalation (`<if_sid>`)**:
   - *Rules 100100 & 100102*: Extend existing parent alerts (default rule `92057` for PowerShell and `92302` for Registry Run keys) to escalate severity (Level 12–15) and enrich alerts with MITRE ATT&CK taxonomy metadata.
2. **Standalone Direct Sysmon Field Matching (`<field name="...">`)**:
   - *Rules 100101, 100103, 100104, & 100105*: Inspect raw Sysmon Event ID 1 process creation fields directly (`win.system.eventID: ^1$`, `win.eventdata.image`, PCRE2 regex on `win.eventdata.commandLine`).

---

## 🧪 Rule Validation & Test Fixtures

Test fixtures and true/false-positive control samples are documented in [`tests/logtest_samples.json`](tests/logtest_samples.json). Run `python3 tests/run_tests.py` to execute XML syntax checks and logtest event sample coverage assertions.

---

## 📑 Detailed Incident Response Reports

- 📄 [**IR-001: PowerShell Obfuscation (T1059.001)**](incident_reports/IR-001_T1059.001_PowerShell_Obfuscation.md)
- 📄 [**IR-002: Scheduled Task Persistence (T1053.005)**](incident_reports/IR-002_T1053.005_Scheduled_Task_Persistence.md)
- 📄 [**IR-003: Registry Run Key Persistence (T1547.001)**](incident_reports/IR-003_T1547.001_Registry_Run_Keys.md)
- 📄 [**IR-004: Clear Windows Event Logs (T1070.001)**](incident_reports/IR-004_T1070.001_Clear_Windows_Event_Logs.md)
- 📄 [**IR-005: Credential Store Enumeration (T1555.004)**](incident_reports/IR-005_T1555.004_Credential_Store_Enumeration.md)

---

## 🏷️ Version History & Release Notes

### `v1.1.0` - Production-Grade Engineering Refinement
- **Rule Tightening**: Enforced exact regex matching (`^1$`) on `win.system.eventID`.
- **Test Suite**: Added python test runner (`tests/run_tests.py`) and true/false positive logtest sample fixtures (`tests/logtest_samples.json`).
- **Telemetry Pinning**: Added pinned `sysmonconfig-export.xml` and durable `atomic_red_team_guide.md` with commit SHA pins.
- **Agent Enrollment**: Documented network ports, client registration, and agent authentication steps.
- **Licensing**: Added MIT License file.

---

## 📜 License & Acknowledgments

This project is released under the [MIT License](LICENSE). Special thanks to:
- [Wazuh SIEM](https://wazuh.com)
- [Microsoft Sysinternals Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [Red Canary Atomic Red Team](https://github.com/redcanaryco/invoke-atomicredteam)
