#!/bin/bash
set -e

ALL_TESTS=("sql" "analyst" "complete" "agentic")

if [ "$#" -gt 0 ]; then
  TESTS=("$@")
else
  TESTS=("${ALL_TESTS[@]}")
fi

for name in "${TESTS[@]}"; do
  test_path="tests/$name/tests.py"
  if [ -f "$test_path" ]; then
    echo
    echo "=== Rodando $test_path ==="
    python "$test_path"
  else
    echo
    echo "Arquivo não encontrado: $test_path"
  fi
done

echo
echo "Execução concluída."
