#!/bin/bash

# Define service name and paths
SERVICE_NAME="keylogger-detection-backend"
PID_FILE="/tmp/${SERVICE_NAME}.pid"
LOG_FILE="$HOME/backend.log"
VENV_PATH="$HOME/venv"
PORT=8000

# Function to check if the port is in use
is_port_in_use() {
    netstat -tuln | grep ":$PORT " > /dev/null
    return $?
}

# Function to check if service is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            return 0  # Running
        fi
    fi
    
    # Double-check with pgrep as fallback
    if pgrep -f "uvicorn backend:app" > /dev/null; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Function to find what's using port 8000
check_port_usage() {
    echo "Checking what's using port $PORT..."
    lsof -i :$PORT || netstat -tuln | grep ":$PORT "
    
    echo "Processes that might be related to our service:"
    pgrep -f "uvicorn|backend:app" | while read pid; do
        echo "PID $pid: $(ps -p $pid -o command=)"
    done
}

# Function to force kill anything on our port
force_kill_port() {
    echo "Force killing any process using port $PORT..."
    fuser -k $PORT/tcp 2>/dev/null
    
    # Also try to kill any uvicorn process
    pkill -f "uvicorn backend:app" 2>/dev/null
    
    sleep 2
    if is_port_in_use; then
        echo "WARNING: Port $PORT is still in use after kill attempt."
        check_port_usage
        return 1
    else
        echo "Port $PORT is now available."
        return 0
    fi
}

# Function to start the service in the background
start_service() {
    # First, check if already running by our detection
    if is_running; then
        echo "Service is already running according to process checks."
        return
    fi
    
    # Then check if port is in use
    if is_port_in_use; then
        echo "ERROR: Port $PORT is already in use, but service is not detected as running."
        check_port_usage
        echo ""
        echo "Options:"
        echo "1. Run './backend-service.sh kill-port' to force close anything on port $PORT"
        echo "2. Manually kill the processes shown above"
        echo "3. Change the port in this script"
        return 1
    fi
    
    echo "Starting $SERVICE_NAME in the background..."
    
    # Clear previous log
    > "$LOG_FILE"
    
    # Activate virtual environment and start service
    source "$VENV_PATH/bin/activate"
    nohup uvicorn backend:app --host 0.0.0.0 --port $PORT --reload > "$LOG_FILE" 2>&1 &
    
    # Save PID
    echo $! > "$PID_FILE"
    
    # Verify it started
    sleep 2
    if is_running; then
        echo "$SERVICE_NAME started successfully."
        if ! is_port_in_use; then
            echo "WARNING: Service process is running but port $PORT is not in use yet."
        fi
    else
        echo "Failed to start $SERVICE_NAME. Check logs at $LOG_FILE."
        cat "$LOG_FILE"
    fi
}

# Function to start service in the foreground (console mode)
start_console() {
    if is_running; then
        echo "Service is already running in the background. Stop it first."
        return 1
    fi
    
    if is_port_in_use; then
        echo "ERROR: Port $PORT is already in use."
        check_port_usage
        return 1
    fi
    
    echo "Starting $SERVICE_NAME in console mode (Ctrl+C to stop)..."
    
    # Activate virtual environment and start service in foreground
    source "$VENV_PATH/bin/activate"
    uvicorn backend:app --host 0.0.0.0 --port $PORT
}

# Function to show real-time logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo "Showing real-time logs (Ctrl+C to exit):"
        tail -f "$LOG_FILE"
    else
        echo "Log file not found. Is the service running in background mode?"
    fi
}

# Function to stop the service
stop_service() {
    echo "Stopping $SERVICE_NAME..."
    
    local found=false
    
    # Get all PIDs for the service
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "Sending SIGTERM to process $PID (from PID file)..."
            kill -15 "$PID" 2>/dev/null
            found=true
        fi
    fi
    
    # Also check with pgrep
    for PID in $(pgrep -f "uvicorn backend:app"); do
        echo "Sending SIGTERM to process $PID (from pgrep)..."
        kill -15 "$PID" 2>/dev/null
        found=true
    done
    
    if [ "$found" = false ]; then
        echo "No running processes found for $SERVICE_NAME."
        if is_port_in_use; then
            echo "However, port $PORT is still in use by something."
            check_port_usage
        fi
        rm -f "$PID_FILE" 2>/dev/null
        return
    fi
    
    # Wait for it to stop
    local COUNT=0
    while (is_running || is_port_in_use) && [ $COUNT -lt 10 ]; do
        sleep 1
        COUNT=$((COUNT+1))
    done
    
    # If still running, force kill
    if is_running || is_port_in_use; then
        echo "Service didn't stop gracefully. Forcing shutdown..."
        force_kill_port
    fi
    
    # Clean up PID file
    rm -f "$PID_FILE" 2>/dev/null
    
    # Final check
    if ! is_running && ! is_port_in_use; then
        echo "$SERVICE_NAME stopped successfully."
    else
        echo "WARNING: Could not fully stop $SERVICE_NAME."
        check_port_usage
    fi
}

# Function to check service status
check_status() {
    if is_running; then
        PID=$(cat "$PID_FILE" 2>/dev/null || pgrep -f "uvicorn backend:app" | head -1)
        echo "$SERVICE_NAME is running (PID: $PID)"
        echo "Log file: $LOG_FILE"
    else
        echo "$SERVICE_NAME is not running."
    fi
    
    if is_port_in_use; then
        echo "Port $PORT is in use."
        check_port_usage
    else
        echo "Port $PORT is available."
    fi
}

# Process command line arguments
case "$1" in
    start)
        start_service
        ;;
    console)
        start_console
        ;;
    logs)
        show_logs
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        sleep 2
        start_service
        ;;
    status)
        check_status
        ;;
    check-port)
        check_port_usage
        ;;
    kill-port)
        force_kill_port
        ;;
    *)
        echo "Usage: $0 {start|console|logs|stop|restart|status|check-port|kill-port}"
        echo ""
        echo "Commands:"
        echo "  start      - Start the service in the background"
        echo "  console    - Start in foreground with logs to console"
        echo "  logs       - Show real-time logs from the background service"
        echo "  stop       - Stop the running service"
        echo "  restart    - Restart the service"
        echo "  status     - Check if service is running"
        echo "  check-port - See what's using port $PORT"
        echo "  kill-port  - Force kill anything using port $PORT"
        exit 1
        ;;
esac

exit 0