# 🛡️ Detection Engineering & Threat Hunting Lab (Wazuh + Sysmon + MITRE ATT&CK)

> A hands-on SOC detection engineering lab built to simulate real-world cyber attack techniques, analyze endpoint telemetry via Sysmon, author custom Wazuh SIEM detection rules, and perform structured incident response.

---

## 🎯 Lab Overview & Objectives

The primary goal of this project is to gain end-to-end hands-on experience as a **Detection Engineer / SOC Analyst**:
1. **Attack Execution**: Personally execute real-world adversary techniques using **Atomic Red Team** scripts and command-line LOLBins inside a target Windows 11 environment.
2. **Log Enrichment**: Capture high-fidelity endpoint process creation and system telemetry using **Microsoft Sysmon**.
3. **SIEM Ingestion & Rule Engineering**: Forward telemetry to a locally hosted **Wazuh SIEM Manager** and engineer custom XML detection rules mapped to the **MITRE ATT&CK Framework**.
4. **Incident Response**: Conduct threat hunting and produce structured incident reports complete with containment strategies.

---

## 🏗️ Architecture & Component Design

```
+-----------------------------------------------------------------------------------+
|                                 YOUR HOST (Mac)                                   |
|                                                                                   |
|   +---------------------------------------+                                       |
|   |         Wazuh Manager (Docker)        |                                       |
|   |   - Dashboard: https://localhost      |                                       |
|   |   - Custom Rules: local_rules.xml     |                                       |
|   +---------------------------------------+                                       |
|                       ^                                                           |
|                       | Log Forwarding (Sysmon / Port 1514)                       |
|                       v                                                           |
|   +---------------------------------------+                                       |
|   |    Target Endpoint (Windows 11 VM)    |                                       |
|   |   - Sysmon (SwiftOnSecurity Baseline) |                                       |
|   |   - Wazuh Agent (v4.x)                |                                       |
|   |   - Atomic Red Team Test Suite        |                                       |
|   +---------------------------------------+                                       |
+-----------------------------------------------------------------------------------+
```

### Infrastructure Specs
- **SIEM Manager**: Wazuh Manager (Self-Hosted via Docker on Host OS)
- **Monitored Endpoint**: Windows 11 Pro Virtual Machine (VirtualBox NAT Network)
- **Telemetry Engine**: Microsoft Sysmon (`Microsoft-Windows-Sysmon/Operational`)
- **Attack Automation**: Red Canary Atomic Red Team

---

## 📊 MITRE ATT&CK Detection Matrix

Below is the summary of the 5 core attack scenarios executed, detected, and verified with custom Wazuh XML rules:

| # | Technique Name | MITRE ID | Tactic | Parent Rule | Custom Rule ID | Severity | Status |
|---|---|---|---|---|---|---|---|
| **1** | Base64 Encoded PowerShell | `T1059.001` | Execution | `92057` | **`100100`** | Level 15 (Critical) | ✅ Verified |
| **2** | Scheduled Task Creation | `T1053.005` | Persistence | `92032` | **`100101`** | Level 12 (High) | ✅ Verified |
| **3** | Registry Run Key Persistence | `T1547.001` | Persistence | `92302` | **`100102`** | Level 12 (High) | ✅ Verified |
| **4** | Clear Windows Event Logs | `T1070.001` | Defense Evasion | `windows` | **`100103`** | Level 13 (High) | ✅ Verified |
| **5** | Credential Store Enumeration | `T1555.004` | Credential Access | `windows` | **`100104`** | Level 14 (High) | ✅ Verified |

---

## 🛠️ Repository Layout

```text
.
├── custom_rules/
│   └── local_rules.xml                # Custom Wazuh detection rules (Rules 100100 - 100104)
├── incident_reports/
│   ├── IR-001_T1059.001_PowerShell_Obfuscation.md
│   ├── IR-002_T1053.005_Scheduled_Task_Persistence.md
│   ├── IR-003_T1547.001_Registry_Run_Keys.md
│   ├── IR-004_T1070.001_Clear_Windows_Event_Logs.md
│   └── IR-005_T1555.004_Credential_Store_Enumeration.md
├── queries/
│   └── threat_hunting.md              # DQL threat hunting queries & search cheat sheet
└── configs/
    ├── sysmon_config_note.md          # Sysmon event logging baseline documentation
    └── wazuh_agent_ossec_snippet.xml  # ossec.conf Sysmon eventchannel binding snippet
```

---

## 🚀 How to Reproduce

### 1. Deploy Wazuh SIEM Manager
Run Wazuh locally via Docker:
```bash
docker run -d --name wazuh.manager -p 1514:1514 -p 55000:55000 -p 443:443 wazuh/wazuh-manager:latest
```

### 2. Configure Sysmon on Windows Endpoint
1. Install Sysmon on the Windows 11 VM:
   ```cmd
   sysmon64.exe -i sysmonconfig-export.xml -accepteula
   ```
2. Edit `C:\Program Files (x86)\ossec-agent\ossec.conf` and append the Sysmon eventchannel binding:
   ```xml
   <localfile>
     <location>Microsoft-Windows-Sysmon/Operational</location>
     <log_format>eventchannel</log_format>
   </localfile>
   ```
3. Restart the Wazuh service (`net stop wazuh && net start wazuh`).

### 3. Deploy Custom Rules
Append the rules in [`custom_rules/local_rules.xml`](custom_rules/local_rules.xml) into `/var/ossec/etc/rules/local_rules.xml` on the Wazuh Manager (or via **Server Management -> Rules** in the Web UI) and restart the manager.

### 4. Execute Attacks & Verify Detections
Run the corresponding Atomic Red Team commands or native CLI scripts on Windows 11 (e.g. `cmdkey /list`, `wevtutil cl System`, `schtasks /create...`), and monitor alerts in the Wazuh Threat Hunting dashboard filtering by `rule.id: 100100 - 100104`.

---

## 📑 Detailed Incident Reports

Detailed incident analysis reports for each technique are available in the [`incident_reports/`](incident_reports/) directory:
- [IR-001: PowerShell Obfuscation (T1059.001)](incident_reports/IR-001_T1059.001_PowerShell_Obfuscation.md)
- [IR-002: Scheduled Task Persistence (T1053.005)](incident_reports/IR-002_T1053.005_Scheduled_Task_Persistence.md)
- [IR-003: Registry Run Key Persistence (T1547.001)](incident_reports/IR-003_T1547.001_Registry_Run_Keys.md)
- [IR-004: Clear Windows Event Logs (T1070.001)](incident_reports/IR-004_T1070.001_Clear_Windows_Event_Logs.md)
- [IR-005: Credential Store Enumeration (T1555.004)](incident_reports/IR-005_T1555.004_Credential_Store_Enumeration.md)

---

## 📜 License & Acknowledgments

This project is built for educational, portfolio, and defensive research purposes. Special thanks to the open-source projects:
- [Wazuh SIEM](https://wazuh.com)
- [Microsoft Sysinternals Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [Red Canary Atomic Red Team](https://github.com/redcanaryco/invoke-atomicredteam)
