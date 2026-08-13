# Sysmon Integration Configuration

## Endpoint Setup

- **Host Machine**: Windows 11 Pro (VirtualBox Target VM)
- **Agent**: Wazuh Windows Agent (v4.x)
- **Log Source**: Microsoft-Windows-Sysmon/Operational

## Key Event Types Monitored

1. **Process Creation (Event ID 1)**: Captures process start events, binary hashes (MD5, SHA256), parent process GUIDs, and full execution command lines.
2. **Network Connections (Event ID 3)**: Monitors inbound and outbound TCP/UDP connections.
3. **Registry Events (Event IDs 12, 13, 14)**: Tracks registry key and value modifications (specifically autostart / run keys).
4. **Scheduled Task Operations**: Monitored via command line process telemetry and Windows TaskScheduler operational logs.

## Configuration Baseline

- Sysmon was deployed using the industry-standard baseline configuration (SwiftOnSecurity ruleset).
- Windows Event Log forwarding to Wazuh Manager was enabled via `<localfile>` eventchannel binding in `ossec.conf`.
