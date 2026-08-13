# Durable Atomic Red Team Execution & Verification Guide

This document provides durable, reproducible execution specifications for all attack scenarios tested in this lab.

---

## 📌 Environment & Dependency Pins

- **Invoke-AtomicRedTeam Module**: `v3.1.0` Tagged Release
- **Atomics Repository Commit Pin**: `RedCanary/atomic-red-team@e43d93b922a84a600a74adbfbbdbfcaeb0453d86` (Immutable SHA)
- **Atomics Local Installation Path**: `C:\AtomicRedTeam\atomics\atomics`

---

## ⚔️ Attack Scenarios & Execution Matrix

### 1. Technique T1059.001 - Obfuscated Base64 PowerShell
- **Atomic Test Name**: PowerShell Base64 Encoded Command
- **Test GUID**: `ef938fa2-68b6-455b-8d18-2e06c3a10526`
- **Execution Command**:
  ```powershell
  Set-ExecutionPolicy Bypass -Scope Process -Force
  Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
  Invoke-AtomicTest T1059.001 -TestNumbers 17 -PathToAtomicsFolder "C:\AtomicRedTeam\atomics\atomics"
  ```
- **Cleanup Command**: None required (stateless execution).
- **Expected Alert IDs**: `Rule 100100` (Parent correlation) & `Rule 100105` (Standalone field matching).

---

### 2. Technique T1053.005 - Scheduled Task Creation
- **Atomic Test Name**: Scheduled Task Local
- **Test GUID**: `b9f315be-04ef-4015-8f6b-9d4cb7d8a631`
- **Execution Command**:
  ```powershell
  Invoke-AtomicTest T1053.005 -TestNumbers 2 -PathToAtomicsFolder "C:\AtomicRedTeam\atomics\atomics"
  ```
- **Cleanup Command**:
  ```powershell
  Invoke-AtomicTest T1053.005 -TestNumbers 2 -PathToAtomicsFolder "C:\AtomicRedTeam\atomics\atomics" -Cleanup
  ```
- **Expected Alert ID**: `Rule 100101`.

---

### 3. Technique T1547.001 - Registry Run Key Persistence
- **Atomic Test Name**: RegKey Persistence - CurrentVersion Run
- **Test GUID**: `39b369ad-ee1f-4efc-8f1d-cfd90ee462b2`
- **Execution Command**:
  ```powershell
  Invoke-AtomicTest T1547.001 -TestNumbers 1 -PathToAtomicsFolder "C:\AtomicRedTeam\atomics\atomics"
  ```
- **Cleanup Command**:
  ```powershell
  Invoke-AtomicTest T1547.001 -TestNumbers 1 -PathToAtomicsFolder "C:\AtomicRedTeam\atomics\atomics" -Cleanup
  ```
- **Expected Alert ID**: `Rule 100102`.

---

### 4. Technique T1070.001 - Clear Windows Event Logs
- **Atomic Test Name**: Clear Logs via wevtutil
- **Test GUID**: `a88be08e-5b12-4217-bf48-18e38d7c2e0b`
- **Execution Command**:
  ```powershell
  wevtutil cl System
  ```
- **Cleanup Command**: None required.
- **Expected Alert ID**: `Rule 100103`.

---

### 5. Technique T1555.004 - Windows Credential Store Enumeration
- **Atomic Test Name**: Cmdkey Saved Credentials Listing
- **Test GUID**: `d24d2629-45d6-4447-b248-6a56f082e6ef`
- **Execution Command**:
  ```cmd
  cmdkey.exe /list
  ```
- **Cleanup Command**: None required.
- **Expected Alert ID**: `Rule 100104`.
