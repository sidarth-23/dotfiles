#!/usr/bin/env python3
"""
Lint Check Hook - Runs linting and instructs Claude to fix errors
Supports multiple linters and package managers
"""
import sys
import json
import os
import subprocess

# Lock file to package manager mapping
LOCK_FILE_TO_PM = {
    "pnpm-lock.yaml": "pnpm",
    "package-lock.json": "npm",
    "yarn.lock": "yarn",
    "bun.lockb": "bun",
}

# Linter configurations: (config_file, lint_command_suffix)
LINTER_CONFIGS = {
    "eslint": {
        "configs": [".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml", "eslint.config.js", "eslint.config.mjs"],
        "command": "eslint . --format stylish",
        "fix_command": "eslint . --fix",
    },
    "biome": {
        "configs": ["biome.json", "biome.jsonc"],
        "command": "biome check .",
        "fix_command": "biome check . --fix",
    },
    "prettier": {
        "configs": [".prettierrc", ".prettierrc.js", ".prettierrc.json", "prettier.config.js"],
        "command": "prettier --check .",
        "fix_command": "prettier --write .",
    },
    "stylelint": {
        "configs": [".stylelintrc", ".stylelintrc.js", ".stylelintrc.json", "stylelint.config.js"],
        "command": "stylelint '**/*.css'",
        "fix_command": "stylelint '**/*.css' --fix",
    },
    "tsc": {
        "configs": ["tsconfig.json"],
        "command": "tsc --noEmit",
        "fix_command": None,  # TypeScript errors need manual fixing
    },
}


def is_js_project(working_dir="."):
    """Check if the current directory is a JavaScript/Node.js project"""
    js_indicators = ["package.json", "node_modules", "tsconfig.json", "jsconfig.json"]
    for indicator in js_indicators:
        if os.path.exists(os.path.join(working_dir, indicator)):
            return True
    return False


def detect_package_manager(working_dir="."):
    """Detect the project's package manager based on lock file"""
    for lock_file, pm in LOCK_FILE_TO_PM.items():
        if os.path.exists(os.path.join(working_dir, lock_file)):
            return pm
    return "npm"  # Default to npm


def detect_linters(working_dir="."):
    """Detect which linters are configured in the project"""
    detected = []

    # Check for config files
    for linter, config in LINTER_CONFIGS.items():
        for config_file in config["configs"]:
            if os.path.exists(os.path.join(working_dir, config_file)):
                detected.append(linter)
                break

    # Check package.json for lint scripts and dependencies
    pkg_json_path = os.path.join(working_dir, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            with open(pkg_json_path, "r") as f:
                pkg = json.load(f)

                # Check devDependencies
                dev_deps = pkg.get("devDependencies", {})
                deps = pkg.get("dependencies", {})
                all_deps = {**deps, **dev_deps}

                for linter in LINTER_CONFIGS.keys():
                    if linter in all_deps and linter not in detected:
                        detected.append(linter)

                # Check for eslint plugins (indicates eslint usage)
                if any(k.startswith("eslint") for k in all_deps) and "eslint" not in detected:
                    detected.append("eslint")

        except (json.JSONDecodeError, IOError):
            pass

    return detected


def get_lint_script(working_dir="."):
    """Check if there's a lint script in package.json"""
    pkg_json_path = os.path.join(working_dir, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            with open(pkg_json_path, "r") as f:
                pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                if "lint" in scripts:
                    return "lint"
                if "lint:fix" in scripts:
                    return "lint:fix"
        except (json.JSONDecodeError, IOError):
            pass
    return None


def run_lint(pm, working_dir="."):
    """Run linting and return results"""
    results = {
        "success": True,
        "errors": [],
        "linters_run": [],
        "fix_commands": [],
    }

    # First, check for a lint script in package.json
    lint_script = get_lint_script(working_dir)
    if lint_script:
        cmd = f"{pm} run {lint_script}"
        results["linters_run"].append(f"package.json script: {lint_script}")

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode != 0:
                results["success"] = False
                results["errors"].append({
                    "linter": lint_script,
                    "output": result.stdout + result.stderr,
                    "command": cmd,
                })
                if "lint:fix" in get_all_scripts(working_dir):
                    results["fix_commands"].append(f"{pm} run lint:fix")

        except subprocess.TimeoutExpired:
            results["errors"].append({
                "linter": lint_script,
                "output": "Lint command timed out after 120 seconds",
                "command": cmd,
            })
            results["success"] = False
        except Exception as e:
            results["errors"].append({
                "linter": lint_script,
                "output": str(e),
                "command": cmd,
            })
            results["success"] = False

        return results

    # If no lint script, run detected linters directly
    detected_linters = detect_linters(working_dir)

    if not detected_linters:
        results["linters_run"].append("No linters detected")
        return results

    for linter in detected_linters:
        config = LINTER_CONFIGS[linter]
        cmd = f"{pm} exec {config['command']}"
        results["linters_run"].append(linter)

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode != 0:
                results["success"] = False
                results["errors"].append({
                    "linter": linter,
                    "output": result.stdout + result.stderr,
                    "command": cmd,
                })
                if config["fix_command"]:
                    results["fix_commands"].append(f"{pm} exec {config['fix_command']}")

        except subprocess.TimeoutExpired:
            results["errors"].append({
                "linter": linter,
                "output": "Lint command timed out after 120 seconds",
                "command": cmd,
            })
            results["success"] = False
        except Exception as e:
            results["errors"].append({
                "linter": linter,
                "output": str(e),
                "command": cmd,
            })
            results["success"] = False

    return results


def get_all_scripts(working_dir="."):
    """Get all scripts from package.json"""
    pkg_json_path = os.path.join(working_dir, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            with open(pkg_json_path, "r") as f:
                pkg = json.load(f)
                return pkg.get("scripts", {})
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def format_output(results, pm):
    """Format the lint results for Claude"""
    output = []

    output.append("=" * 60)
    output.append("LINT CHECK RESULTS")
    output.append("=" * 60)
    output.append("")
    output.append(f"Linters checked: {', '.join(results['linters_run'])}")
    output.append(f"Status: {'✅ PASSED' if results['success'] else '❌ FAILED'}")
    output.append("")

    if not results["success"]:
        output.append("-" * 60)
        output.append("ERRORS FOUND - Please fix the following issues:")
        output.append("-" * 60)

        for error in results["errors"]:
            output.append("")
            output.append(f"[{error['linter'].upper()}]")
            output.append(f"Command: {error['command']}")
            output.append("")
            output.append(error["output"])
            output.append("")

        output.append("-" * 60)
        output.append("INSTRUCTIONS FOR CLAUDE:")
        output.append("-" * 60)
        output.append("")
        output.append("Please fix the lint errors shown above by:")
        output.append("1. Reading each error message carefully")
        output.append("2. Locating the files mentioned in the errors")
        output.append("3. Making the necessary code changes to fix each issue")
        output.append("4. Running the lint command again to verify fixes")
        output.append("")

        if results["fix_commands"]:
            output.append("Auto-fixable issues can be resolved by running:")
            for cmd in results["fix_commands"]:
                output.append(f"  {cmd}")
            output.append("")
            output.append("For issues that can't be auto-fixed, manually edit the files.")

        output.append("")

    return "\n".join(output)


def main():
    """Main function"""
    working_dir = os.getcwd()

    # Check if this is a JS project
    if not is_js_project(working_dir):
        print("Not a JavaScript project, skipping lint check.")
        sys.exit(0)

    # Detect package manager
    pm = detect_package_manager(working_dir)

    print(f"Running lint check (using {pm})...")
    print("")

    # Run linting
    results = run_lint(pm, working_dir)

    # Output results
    print(format_output(results, pm))

    # Exit with appropriate code
    if results["success"]:
        sys.exit(0)
    else:
        # Exit code 1 indicates errors that need fixing
        sys.exit(1)


if __name__ == "__main__":
    main()
