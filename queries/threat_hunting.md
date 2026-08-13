# Threat Hunting Query Cheat Sheet

Use these DQL (Dashboard Query Language) and KQL (Kibana Query Language) queries in the **Wazuh Threat Hunting** module (`https://localhost/app/threat-hunting`) to locate telemetry, inspect raw alerts, and perform proactive threat hunting.

---

## 🎯 Custom Detection Rules

Search for alerts triggered by custom rules written during this lab:

| Technique | MITRE ID | Rule Type | Wazuh Rule ID | DQL Query |
|---|---|---|---|---|
| Base64 PowerShell | `T1059.001` | Parent Correlation | **100100** | `rule.id: 100100` |
| Base64 PowerShell | `T1059.001` | Standalone Sysmon | **100105** | `rule.id: 100105` |
| Scheduled Task | `T1053.005` | Standalone Sysmon | **100101** | `rule.id: 100101` |
| Registry Run Key | `T1547.001` | Parent Correlation | **100102** | `rule.id: 100102` |
| Clear Event Logs | `T1070.001` | Standalone Sysmon | **100103** | `rule.id: 100103` |
| Credential Enum | `T1555.004` | Standalone Sysmon | **100104** | `rule.id: 100104` |

---

## 🔍 Process Creation & Sysmon Telemetry

Filter raw Sysmon Event ID 1 process creation telemetry:

```text
data.win.system.providerName: "Microsoft-Windows-Sysmon" AND data.win.system.eventID: "1"
```

Find specific binary execution:
```text
data.win.eventdata.image: "*powershell.exe" OR data.win.eventdata.image: "*schtasks.exe" OR data.win.eventdata.image: "*wevtutil.exe" OR data.win.eventdata.image: "*cmdkey.exe"
```

---

## 🚨 High Severity Alerts Filter

Filter all high-severity security alerts across the agent:

```text
agent.name: "WIN11-TARGET" AND rule.level >= 12
```

---

## 🛡️ MITRE ATT&CK Tactic Filtering

Filter events by MITRE tactics:
- **Execution**: `rule.mitre.id: "T1059.001"`
- **Persistence**: `rule.mitre.id: "T1053.005"` OR `rule.mitre.id: "T1547.001"`
- **Defense Evasion**: `rule.mitre.id: "T1070.001"`
- **Credential Access**: `rule.mitre.id: "T1555.004"`
