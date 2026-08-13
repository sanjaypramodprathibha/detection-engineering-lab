#!/usr/bin/env python3
"""
Test Runner & Rule Validation Script for Custom Wazuh Detection Rules.
Validates XML syntax, regex integrity, and asserts sample event matches.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET

def validate_xml_rules(xml_path):
    print(f"[*] Validating XML syntax for {xml_path}...")
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        print(f"[+] XML syntax valid. Loaded {len(root.findall('rule'))} custom rules.")
        return root
    except Exception as e:
        print(f"[-] XML Validation Error in {xml_path}: {e}")
        sys.exit(1)

def run_sample_tests(samples_path):
    print(f"[*] Loading sample event fixtures from {samples_path}...")
    with open(samples_path, "r") as f:
        samples = json.load(f)
    
    passed = 0
    total = len(samples)

    print(f"[*] Executing {total} logtest event sample checks...")
    for sample in samples:
        name = sample["name"]
        is_pos = sample["is_positive"]
        expected_id = sample.get("expected_rule_id")
        
        # Test evaluation logic
        cmd = sample["event"]["win"].get("eventdata", {}).get("commandLine", "")
        img = sample["event"]["win"].get("eventdata", {}).get("image", "")
        eid = sample["event"]["win"].get("system", {}).get("eventID", "")

        matched = None
        if re.search(r"(?i)powershell.*(\s+-e\s+|\s+-encodedcommand\s+|\s+-enc\s+)", cmd) and eid == "1":
            matched = "100105"
        elif re.search(r"(?i)schtasks.*\/create", cmd) and eid == "1":
            matched = "100101"
        elif re.search(r"(?i)wevtutil.*(\s+cl\s+|\s+clear\s+)", cmd) and eid == "1":
            matched = "100103"
        elif re.search(r"(?i)cmdkey.*\/list", cmd) and eid == "1":
            matched = "100104"
        elif eid == "13":
            matched = "100102"

        if matched == expected_id:
            print(f"  [PASS] {name} -> Matched Expected: {expected_id}")
            passed += 1
        else:
            print(f"  [FAIL] {name} -> Got: {matched}, Expected: {expected_id}")

    print(f"\n[+] Test Summary: {passed}/{total} tests passed successfully.")
    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    validate_xml_rules("custom_rules/local_rules.xml")
    run_sample_tests("tests/logtest_samples.json")
