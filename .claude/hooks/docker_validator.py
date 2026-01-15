#!/usr/bin/env python3
import sys
import json
import re


def validate_docker_command(tool_use):
    """Validate Docker commands to prevent using inappropriate image name suffixes"""

    if tool_use.get("tool_name") != "Bash":
        sys.exit(0)

    command = tool_use.get("tool_input", {}).get("command", "")

    # Check if it's a docker build command
    if "docker build" in command or "docker tag" in command:
        # Find -t tag parameter
        tag_pattern = r"-t\s+([^\s]+)"
        matches = re.findall(tag_pattern, command)

        for tag in matches:
            # Check if it contains disallowed suffixes (note: latest is allowed)
            bad_suffixes = ["-v2", "-v3", "-test", "-dev", "-prod", "-staging"]
            image_name = tag.split(":")[0]  # Get the image name part

            for suffix in bad_suffixes:
                if image_name.endswith(suffix):
                    clean_name = image_name[: -len(suffix)]
                    tag_part = tag.split(":")[1] if ":" in tag else "latest"
                    error_msg = f"Image name should not use '{suffix}' suffix. Suggested: {clean_name}:{tag_part}"
                    print(error_msg, file=sys.stderr)
                    sys.exit(2)  # Exit code 2 = blocking error


if __name__ == "__main__":
    # Read input
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    validate_docker_command(tool_use)

    # If no issues, exit silently
    sys.exit(0)
