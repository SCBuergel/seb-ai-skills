#!/bin/bash
# Run one skill's eval cases against the working copy.
# Usage: evals/run.sh <skill-name> [extra `claude plugin eval` options]
# `claude plugin eval` needs a plugin directory with a plugin.json, which this
# repository's flat layout does not have, so this builds one in a temp dir.
set -euo pipefail
skill=${1:?skill name}; shift
repo=$(cd "$(dirname "$0")/.." && pwd)
[ -d "$repo/evals/$skill" ] || { echo "no eval cases in evals/$skill" >&2; exit 1; }
tmp=$(mktemp -d)
mkdir -p "$tmp/.claude-plugin" "$tmp/skills"
cp -r "$repo/skills/$skill" "$tmp/skills/"
cp -r "$repo/evals/$skill" "$tmp/evals"
printf '{"name":"%s","version":"0.0.0-eval"}\n' "$skill" > "$tmp/.claude-plugin/plugin.json"
cd "$tmp"
claude plugin eval . --trust-plugin --judge-model sonnet --no-publish "$@"
echo "Results and report: $tmp/evals/results/"
