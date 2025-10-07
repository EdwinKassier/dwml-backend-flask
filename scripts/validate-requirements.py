#!/usr/bin/env python3
"""
Requirements validation script for pre-commit hooks.
Validates requirements.txt for dependency conflicts and syntax issues.
"""

import re
import sys

from packaging import version


def validate_requirements():
    """Validate requirements.txt for basic syntax and known conflicts."""
    try:
        requirements = {}
        conflicts = []

        with open("requirements.txt", "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-i"):
                    # Extract package name and version
                    match = re.match(
                        r"^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)(?:==|>=|<=|>|<|~=)(.+?)(?:;.*)?$",
                        line,
                    )
                    if match:
                        package_name = match.group(1).split("[")[0]
                        version_spec = match.group(2)
                        requirements[package_name] = (version_spec, line_num)

        # Check for known conflicts
        if "packaging" in requirements and "black" in requirements:
            pkg_ver = requirements["packaging"][0]
            if "==" in pkg_ver and version.parse(
                pkg_ver.split("==")[1]
            ) < version.parse("22.0"):
                conflicts.append("packaging version conflicts with black>=22.0")

        # Check for duplicate packages
        seen = set()
        for pkg in requirements:
            if pkg in seen:
                conflicts.append(f"Duplicate package: {pkg}")
            seen.add(pkg)

        if conflicts:
            print("❌ Requirements validation failed:")
            for conflict in conflicts:
                print(f"  - {conflict}")
            return False
        else:
            print(f"✅ Requirements file is valid ({len(requirements)} packages)")
            return True

    except Exception as e:
        print(f"❌ Requirements validation error: {e}")
        return False


if __name__ == "__main__":
    if not validate_requirements():
        sys.exit(1)
