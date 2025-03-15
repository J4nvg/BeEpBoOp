#!/bin/sh
set -e

# Move one level up (adjust if needed)
cd ../

# Load environment variables if .env is present
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

BACKEND_PID=""

cleanup() {
  echo "Cleaning up..."
  if [ -n "$BACKEND_PID" ]; then
    pkill -P "$BACKEND_PID" 2>/dev/null || true
    kill -9 "$BACKEND_PID" 2>/dev/null || true
  fi
  exit 0
}

trap cleanup INT TERM HUP EXIT

setup_backend() {
  echo "Creating and configuring Python venv..."
  cd app/backend
  uv sync
  start_backend
}

start_backend() {
  echo "Starting backend on localhost:8000..."
  uv run uvicorn app.main:app --workers 1 --host localhost --port 8000 &
  BACKEND_PID=$!
  echo "$BACKEND_PID" > ../../.backend.pid
  cd ../..
}

setup_frontend() {
  echo "Installing and building frontend..."
  cd app/frontend
  npm install
  npm run dev
  cd ../..
}

check_venv() {
  [ ! -d ".venv" ] && echo "No .venv found. Please run with 'setup' first." && exit 1
}

# Clean up any old backend PID
if [ -f .backend.pid ]; then
  OLD_PID="$(cat .backend.pid)"
  if [ -n "$OLD_PID" ]; then
    pkill -P "$OLD_PID" 2>/dev/null || true
    kill -9 "$OLD_PID" 2>/dev/null || true
    echo "Removed old backend process $OLD_PID"
  fi
  rm .backend.pid
fi

# Parse command-line arguments
case "$1" in
  "server")
    if [ "$2" = "no-update" ]; then
      check_venv
      start_backend
    else
      setup_backend
    fi
  ;;
  "client")
    if [ "$2" = "no-update" ]; then
      echo "Frontend requires a build step. Please use setup."
    else
      setup_frontend
    fi
  ;;
  "")
    # Default: set up everything, unless "no-update" is passed
    if [ "$2" = "no-update" ]; then
      check_venv
      start_backend
    else
      setup_backend
      setup_frontend
    fi
  ;;
  *)
    echo "Usage: $0 [server|client] [no-update]"
    exit 1
  ;;
esac

# If the backend started, wait on it
if [ -n "$BACKEND_PID" ]; then
  echo "Waiting for backend process..."
  wait "$BACKEND_PID"
fi
