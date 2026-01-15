#!/usr/bin/env python3
"""
Commit Message Filter Hook - Filters specific content in commit messages
Blocks commits containing Claude auto-generated identifiers
"""

import sys
import json
import re


def check_commit_message(command):
    """Check if commit message contains content that needs to be filtered"""

    # Content patterns to be filtered
    blocked_patterns = [
        r"🤖\s*Generated with\s*\[Claude Code\]",
        r"Co-Authored-By:\s*Claude\s*<noreply@anthropic\.com>",
        r"Generated with.*Claude.*Code",
        r"Claude\s*<noreply@anthropic\.com>",
    ]

    # Check if it's a git commit command
    if "git commit" in command:
        for pattern in blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE | re.MULTILINE):
                error_msg = (
                    "❌ Commit message contains auto-generated Claude identifier, please use a custom commit message"
                )
                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Exit code 2 = blocking error


def main():
    """Main function"""
    # Read hook data from stdin
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    # Only process Bash commands
    if tool_use.get("tool_name") != "Bash":
        sys.exit(0)

    command = tool_use.get("tool_input", {}).get("command", "")

    # Check commit message
    check_commit_message(command)

    # If no issues, exit silently
    sys.exit(0)


if __name__ == "__main__":
    main()
