#!/usr/bin/python

import logging, logging.handlers
import time, socket, psutil


def logging_setup(log_fname):
    # TimedRotatingFileHandler
    trf_handler = logging.handlers.TimedRotatingFileHandler(filename=log_fname,
                                                            when="midnight",
                                                            interval=1,
                                                            backupCount=3)
    console_handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[console_handler, trf_handler])
def send_mail():
    pass

def get_resource_usage(resource: str = 'cpu'):
    """
    This function is used to get resource usage

    Args:
        resource (str): resource type
        'cpu' - cpu usage
        'mem' - memory usage
        'disk' - disk usage

    Returns:
        float: resource usage
    """
    if resource == 'cpu':
        return psutil.cpu_percent(interval=1)
    if resource == 'mem':
        return psutil.virtual_memory().percent
    if resource == 'disk':
        return psutil.disk_usage('/').percent


def get_zombie_processes():
    zombies = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
        if proc.info.get('status') == psutil.STATUS_ZOMBIE:
            zombies.append(proc.info)
    return zombies


def tcp_connection_reachable_check(ip_addr, port, timeout_sec=3, ipv4=True):
    """
    Check the TCP connection of the provided ip_addr, port

    Return:
        bool
        True if reachable else exception

    Params:
        ip_addr: str
            The IP address or hostname
        port : int
            The port number
        timeout_sec: int
            The timeout for the connection attempt in seconds.
        ipv4: bool
            Checking ipv4 protocal: True
            Checking ipv6 protocal: False
    """
    if ipv4:
        protocal = socket.AF_INET
    else:
        protocal = socket.AF_INET6

    sock = socket.socket(protocal, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)

    try:
        sock.connect((ip_addr, port))
        return f"SUCCESS"

    except ConnectionRefusedError:
        # send_mail()
        return f"[ERROR] Connection refused"
    except socket.timeout:
        # send_mail()
        return f"[ERROR] TCP time out"
    except socket.gaierror:
        # send_mail()
        return "[ERROR] DNS ERROR"
    except Exception as e:
        # send_mail()
        return e
    finally:
        sock.close()


def resources_monitor(cpu_threshold=80, mem_threshold=80, disk_threshold=80):
    cpu = get_resource_usage('cpu')
    mem = get_resource_usage('mem')
    disk = get_resource_usage('disk')

    logging.info(f"CPU:{cpu:.2f}%, MEM:{mem:.2f}%, Disk:{disk:.2f}%")

    if cpu > cpu_threshold:
        logging.warning(f"High CPU Usage: {cpu:.2f}%")
        # send_mail()

    if mem > mem_threshold:
        logging.warning(f"High MEM Usage: {mem:.2f}%")
        # send_mail()

    if disk > disk_threshold:
        logging.warning(f"High Disk Usage: {disk:.2f}%")
        # send_mail()


def zombies_detection():
    zombies_lst = get_zombie_processes()
    if zombies_lst:
        logging.warning(f"{len(zombies_lst)} Zombies Detected")

        for z in zombies_lst:
            logging.warning(f"Zombie PID: {z['pid']}, Process Name:{z['name']}, username:{z['username']}")
            # send_mail()


def network_monitor(network_targets, timeout_sec=1, ipv4=True):
    """
    Paramenter:
    network_targets: list

    Example:
        network_targets = [{"type": "Internal", "addr": "2001:b000:168::2 ", "port": 53},
        {"type": "External", "addr": "www.graid.com", "port": 80}]
    """
    for target in network_targets:
        type = target['type']
        addr = target['addr']
        port = target['port']

        result = tcp_connection_reachable_check(addr, port, timeout_sec, ipv4)
        # print(f"{type} result: {result}")

        if result == "SUCCESS":
            logging.info(f"{type} connection to| host = {addr} | port = {port}| OK")

        else:
            logging.error(f"{type} connection to| host = {addr}| port = {port}| {result}")


if __name__ == "__main__":
    log_fname = "/var/log/monitoring_agent.log"
    logging_setup(log_fname)
    logging.info("===== Monitoring Agent Started =====")

    network_targets = [{"type": "Internal", "addr": "192.168.1.254", "port": 53},
                       {"type": "Internal", "addr": "192.168.64.1", "port": 53},
                       {"type": "External", "addr": "www.graid.com", "port": 80},
                       {"type": "External", "addr": "www.qut.edu.au", "port": 443}]
    while True:
        try:
            resources_monitor(cpu_threshold=80, mem_threshold=80, disk_threshold=80)
            zombies_detection()
            network_monitor(network_targets, timeout_sec=1, ipv4=True)
        except Exception as e:
            logging.exception(f"Unexpected Error: {e}")

        time.sleep(60)
