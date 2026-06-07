# Linux Monitoring Agent

A lightweight monitoring agent written in Python for Linux servers.

## Architecture
```text
                                +---------------------------+
                                |     systemd service       |
                                +------------+--------------+
                                             |
                                             v     
                                    +-------------------+
                                    | monitor_agent.py  |
                                    +---------+---------+
                                              |
               ----------------------------------------------------------------
               |                              |                               |
               v                              v                               v
        +------------------+      +---------------------+          +--------------------+
        |resources_monitor |      | zombies_detection   |          |   network_monitor  |
        +------------------+       +---------------------+         +--------------------+
               |                              |                               |
               v                              v                               v
      get_resource_usage()           get_zombie_processes()     tcp_connection_reachable_check()
                     |                        |                               |
                      +-----------------------+------------------------------+
                                              |
                                              v
                                +--------------------------------+
                                |            logging             |
                                |     system log / file log      |
                                +--------------------------------+
```
## Features

### Resource Monitoring
- CPU Utilization
- Memory Usage
- Disk Usage
- Zombie Process Detection

### Network Diagnostics
- TCP Connectivity Check
- DNS Resolution Failure Detection
- TCP Timeout Detection
- Connection Refused Detection

### Logging
- Local log file
- Daily log rotation

### Service Management
- systemd service support
- service starts automatically on reboot
- Automatic restart on failure

---
## Docker Image
The docker image for demonstration has been built and push to docker hub.

The **monitoring agent** can be run easily on your docker with the following command 
```bash
docker run --name monitoring_agent wickedeleanor/monitoring_agent:latest 
```

If docker image does not work on your side, then the following instruction to run the script may be another solution.

---

## Requirements
- Find requirement.txt 
- Mainly
  - Python 3.9+
  - psutil

## Installation

Install dependency:
```bash
python -m pip install psutil

```
Make the python script executable:

```bash
chmod u+x ./monitoring_agent.py
```

## Run Manually

```bash
python3 monitoring_agent.py
```
or simply run
```bash
./monitoring_agent.py
```

## Systemd Configuration
Setting up the **systemd service unit file**:
```bash
cp monitoring_agent.service /etc/systemd/system
```

Make sure it is executable
```bash
chmod u+x /etc/systemd/system/monitoring_agent.service
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable service:

```bash
sudo systemctl enable monitor-agent
```

Start service:

```bash
sudo systemctl start monitor-agent
```

Check status:

```bash
sudo systemctl status monitor-agent
```

---
## Log

Log Location
```bash
/var/log/monitoring_agent.py
```

Log Example
```text
2026-06-06 13:22:05,480 [INFO] ===== Monitoring Agent Started =====
2026-06-06 13:22:06,486 [INFO] CPU:12.60%, MEM:60.20%, Disk:14.20%
2026-06-06 13:22:06,554 [ERROR] Internal connection to| host = 192.168.1.254| port = 53| [Errno 65] No route to host
2026-06-06 13:22:07,555 [ERROR] Internal connection to| host = 192.168.64.1| port = 53| [ERROR] TCP time out
```

## Future Improvements
- Email notification on critical events
- Slack notifications
- Prometheus exporter