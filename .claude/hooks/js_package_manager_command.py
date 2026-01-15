#!/usr/bin/env python3
"""
Package Manager Command Hook - Enforces correct package manager in Bash commands
"""
import sys
import json
import os
import re

LOCK_FILE_TO_PM = {
    "pnpm-lock.yaml": "pnpm",
    "package-lock.json": "npm",
    "yarn.lock": "yarn",
    "bun.lockb": "bun",
}

# Command patterns (excluding executor/dlx commands)
PM_COMMAND_PATTERNS = {
    "npm": r'\bnpm\s+(?!dlx\b)',
    "pnpm": r'\bpnpm\s+(?!dlx\b)',
    "yarn": r'\byarn\s+(?!dlx\b)',
    "bun": r'\bbun\s+(?!x\b)',
}

# Executor commands - always allowed
EXECUTOR_PATTERNS = [
    r'\bnpx\s',
    r'\bpnpm\s+dlx\s',
    r'\byarn\s+dlx\s',
    r'\bbunx\s',
    r'\bbun\s+x\s',
]


def is_js_project(working_dir="."):
    js_indicators = ["package.json", "node_modules", "tsconfig.json", "jsconfig.json"]
    return any(os.path.exists(os.path.join(working_dir, f)) for f in js_indicators)


def detect_package_manager(working_dir="."):
    for lock_file, pm in LOCK_FILE_TO_PM.items():
        if os.path.exists(os.path.join(working_dir, lock_file)):
            return pm

    pkg_json_path = os.path.join(working_dir, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            with open(pkg_json_path, "r") as f:
                pkg = json.load(f)
                pm_field = pkg.get("packageManager", "")
                for pm in ["pnpm", "npm", "yarn", "bun"]:
                    if pm_field.startswith(pm):
                        return pm
        except (json.JSONDecodeError, IOError):
            pass
    return None


def is_executor_command(command):
    return any(re.search(p, command, re.IGNORECASE) for p in EXECUTOR_PATTERNS)


def get_conflicting_pm(command, expected_pm):
    if is_executor_command(command):
        return None
    for pm, pattern in PM_COMMAND_PATTERNS.items():
        if pm != expected_pm and re.search(pattern, command, re.IGNORECASE):
            return pm
    return None


def main():
    if not is_js_project():
        sys.exit(0)

    expected_pm = detect_package_manager()
    if not expected_pm:
        sys.exit(0)

    tool_use = json.loads(sys.stdin.read())
    command = tool_use.get("tool_input", {}).get("command", "")

    conflicting_pm = get_conflicting_pm(command, expected_pm)
    if conflicting_pm:
        print(f"❌ Wrong package manager!", file=sys.stderr)
        print(f"   This repository uses: {expected_pm}", file=sys.stderr)
        print(f"   You tried to use: {conflicting_pm}", file=sys.stderr)
        print(f"   Please use '{expected_pm}' instead.", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
