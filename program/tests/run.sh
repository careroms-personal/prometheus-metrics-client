#!/bin/bash

PROMETHEUS=false
MIMIR=false
URL=""
API_QUERY_PATH="/api/v1"
TEST_CASE_SUIT=""

while [ $# -gt 0 ]; do
  case "$1" in
    -p|--prometheus)
      if [ "$MIMIR" = true ]; then
        echo "Error: Cannot use both -p (Prometheus) and -m (Mimir)"
        exit 1 
      fi
      PROMETHEUS=true
      shift
    ;;

    -m|--mimir)
      if [ "$PROMETHEUS" = true ]; then
        echo "Error: Cannot use both -p (Prometheus) and -m (Mimir)"
        exit 1
      fi
      MIMIR=true
      shift
    ;;

    -u|--url)
      if [ -z "$2" ]; then
        echo "Error: -u requires an argument"
        exit 1
      fi
      URL="$2"
      shift 2
    ;;

    -api|--api-query-path)
      API_QUERY_PATH="$2"
      shift 2
    ;;

    -ts|--test-suit)
      TEST_CASE_SUIT="$2"
      shift 2
    ;;

    *)
      echo "Unknown option: $1"
      exit 1
    ;;
  esac
done

if [ "$PROMETHEUS" = false ] && [ "$MIMIR" = false ]; then
  echo "Error: Must specify either -p (Prometheus) or -m (Mimir)"
  exit 1
fi

# Validate test suite is provided
if [ -z "$TEST_CASE_SUIT" ]; then
  echo "Error: -ts (test suite) is required"
  exit 1
fi

# Validate test suite directory exists
if [ ! -d "$TEST_CASE_SUIT" ]; then
  echo "Error: Test suite directory '$TEST_CASE_SUIT' does not exist"
  exit 1
fi

if [ "$PROMETHEUS" = true ]; then
  echo "Using Prometheus"
  FINAL_PATH="$API_QUERY_PATH"
elif [ "$MIMIR" = true ]; then
  echo "Using Mimir"
  FINAL_PATH="/prometheus$API_QUERY_PATH"
fi

URL="$URL" API_PATH="$FINAL_PATH" python3 "$TEST_CASE_SUIT/main.py"