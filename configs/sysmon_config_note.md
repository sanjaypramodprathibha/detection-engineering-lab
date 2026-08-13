# Sysmon Integration & Telemetry Baseline

## Endpoint Setup & Configuration

- **Host Machine**: Windows 11 Pro (VirtualBox Target VM)
- **Agent**: Wazuh Windows Agent (v4.7.2)
- **Log Channel**: `Microsoft-Windows-Sysmon/Operational`
- **Pinned Sysmon Config**: [`configs/sysmonconfig-export.xml`](sysmonconfig-export.xml) (Schema v4.90)

## Monitored Event IDs & Telemetry Schema

| Event ID | Event Name | Description & Filter Logic | Key Event Data Fields |
|---|---|---|---|
| **Event ID 1** | Process Creation | Captures binary execution, CLI arguments, parent-child process chains, and cryptographic hashes (`MD5`, `SHA256`, `IMPHASH`). | `image`, `commandLine`, `parentImage`, `parentCommandLine`, `user`, `hashes` |
| **Event ID 3** | Network Connection | Monitors inbound and outbound TCP/UDP socket connections. | `image`, `destinationIp`, `destinationPort`, `user` |
| **Event ID 12/13/14** | Registry Events | Tracks autostart registry modifications under `CurrentVersion\Run` and `RunOnce`. | `targetObject`, `eventType`, `image`, `details` |

## Deployment Command
```cmd
sysmon64.exe -i sysmonconfig-export.xml -accepteula
```
