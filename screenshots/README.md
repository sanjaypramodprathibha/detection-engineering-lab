# Screenshot Directory & Visual Assets Guide

This directory holds the high-resolution screenshots and visual evidence for the **Detection Engineering Lab**.

## 📸 Required Screenshot Files

Place your saved PNG screenshots in this folder with the following exact names so they display automatically in `README.md` and `incident_reports/`:

| Filename | Description | Location Displayed |
|---|---|---|
| `architecture.png` | Network & VM Architecture Diagram | `README.md` Architecture Section |
| `dashboard.png` | Main Wazuh Security Events Dashboard Overview | `README.md` Overview |
| `threat_hunting.png` | Wazuh Threat Hunting Events View (`rule.id: 100100 - 100104`) | `README.md` & `queries/threat_hunting.md` |
| `custom_rule.png` | Wazuh Web UI Editor showing `local_rules.xml` | `README.md` Rules Section |
| `powershell_alert.png` | Raw JSON Alert View for Rule `100100` (T1059.001) | `IR-001_T1059.001_PowerShell_Obfuscation.md` |
| `scheduled_task.png` | Raw JSON Alert View for Rule `100101` (T1053.005) | `IR-002_T1053.005_Scheduled_Task_Persistence.md` |
| `registry_alert.png` | Alert View for Rule `100102` (T1547.001) | `IR-003_T1547.001_Registry_Run_Keys.md` |
| `log_clear_alert.png` | Alert View for Rule `100103` (T1070.001) | `IR-004_T1070.001_Clear_Windows_Event_Logs.md` |
| `cmdkey_alert.png` | Alert View for Rule `100104` (T1555.004) | `IR-005_T1555.004_Credential_Store_Enumeration.md` |
