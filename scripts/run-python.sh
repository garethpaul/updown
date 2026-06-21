#!/bin/sh
set -eu

: "${REPOSITORY_PYTHON:?REPOSITORY_PYTHON must name the reviewed absolute interpreter}"

case $REPOSITORY_PYTHON in
    /*) ;;
    *) printf '%s\n' 'REPOSITORY_PYTHON must be an absolute path' >&2; exit 2 ;;
esac

script=$1
shift

exec "$REPOSITORY_PYTHON" -I -B -c '
import os
import runpy
import sys

script = os.path.realpath(sys.argv[1])
sys.argv = sys.argv[1:]
sys.path.insert(0, os.path.dirname(script))
sys.path.insert(0, os.path.dirname(os.path.dirname(script)))
runpy.run_path(script, run_name="__main__")
' "$script" "$@"
