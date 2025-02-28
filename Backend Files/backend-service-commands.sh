# To start the service
./backend-service.sh start

# To stop the service
./backend-service.sh stop

# To restart the service
./backend-service.sh restart

# To check status
./backend-service.sh status

# For foreground mode (exactly like your current script)
./backend-service.sh console

# To view real-time logs from the background service
./backend-service.sh logs

# First, check what's using the port
./backend-service.sh check-port

# Force kill anything on the port
./backend-service.sh kill-port
