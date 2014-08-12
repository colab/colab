# Set the working application directory
# working_directory "/path/to/your/app"
working_directory "/opt/redmine"

# Unicorn PID file location
# pid "/path/to/pids/unicorn.pid"
pid "/opt/redmine/pids/unicorn.pid"

# Path to logs
# stderr_path "/path/to/log/unicorn.log"
# stdout_path "/path/to/log/unicorn.log"
stderr_path "/opt/redmine/log/unicorn.log"
stdout_path "/opt/redmine/log/unicorn.log"

# Unicorn socket
#listen "/tmp/unicorn.redmine.sock"
listen "/tmp/unicorn.redmine.sock"

# Number of processes
# worker_processes 4
worker_processes 2

# Time-out
timeout 30

