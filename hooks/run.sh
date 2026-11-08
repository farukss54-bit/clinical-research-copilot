#!/bin/sh
# Portable launcher: picks a working Python interpreter (python3, python, py -3).
# On Windows, "python3" is often a Microsoft Store stub that exits non-zero, so
# each candidate is probed before use. If no interpreter works, exit silently:
# the hooks are advisory and must never block a session.
script="$1"
dir="$(dirname "$0")"
for py in "python3" "python" "py -3"; do
  if $py -c "pass" >/dev/null 2>&1; then
    exec $py -I -B "$dir/scripts/$script"
  fi
done
exit 0
