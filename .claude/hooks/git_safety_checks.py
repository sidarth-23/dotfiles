#!/usr/bin/env python3
"""
Git Safety Check Hook - Git Operation Safety Check
Prevents misoperation on sensitive branches and checks sensitive files
"""

import sys
import json
import re


def check_git_command(command):
    """Check the safety of git commands"""
    # Check if using --no-verify to skip hooks - directly block
    # Only detect --no-verify as a command argument, not within quotes or heredoc
    # Method: Exclude content within quotes and heredoc
    import shlex

    # Simple detection: --no-verify as an independent argument (with spaces before/after or at line start/end)
    if re.search(r'(^|\s)--no-verify(\s|$)', command):
        # Further check: ensure it's not within quotes or heredoc
        # Check if it's between -m "..." or <<'EOF' ... EOF
        in_quotes = False
        in_heredoc = False

        # Simplified detection: if command has -m "..." or <<'EOF', check --no-verify position
        msg_match = re.search(r'-m\s+["\'].*?["\']', command)
        heredoc_match = re.search(r'<<["\']?EOF["\']?.*?EOF', command, re.DOTALL)

        verify_pos = command.find('--no-verify')
        safe_in_message = False

        if msg_match and msg_match.start() < verify_pos < msg_match.end():
            safe_in_message = True
        if heredoc_match and heredoc_match.start() < verify_pos < heredoc_match.end():
            safe_in_message = True

        if not safe_in_message:
            print("❌ Using --no-verify to skip Git Hooks validation is prohibited!", file=sys.stderr)
            sys.exit(2)

    # Protected branches
    protected_branches = ["main", "master", "production", "prod", "dev", "alpha"]

    # Dangerous operation patterns (warning only, not blocking)
    dangerous_patterns = [
        (r"git\s+push\s+.*\s+--force", "Force push may overwrite remote history, please confirm operation"),
        (r"git\s+reset\s+--hard", "Hard reset will lose uncommitted changes, please confirm operation"),
        (r"git\s+clean\s+-[fd]", "Clean operation will delete untracked files, please confirm operation"),
    ]

    # Check if operating on protected branches - directly reject
    for branch in protected_branches:
        if f"git push origin :{branch}" in command:
            error_msg = f"❌ Blocked deletion of protected branch '{branch}'"
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Exit code 2 = blocking error

        if re.search(rf"git\s+branch\s+-[dD].*{branch}", command):
            error_msg = f"❌ Blocked deletion of protected branch '{branch}'"
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Exit code 2 = blocking error

    # Only log, don't block (returning None means continue execution)
    return None


def main():
    """Main function"""
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    if tool_use.get("tool_name") != "Bash":
        sys.exit(0)

    command = tool_use.get("tool_input", {}).get("command", "")

    # Only check git commands
    if "git" in command:
        check_git_command(command)  # Will exit(2) directly when issues are found

    # If no issues, exit silently
    sys.exit(0)


if __name__ == "__main__":
    main()
