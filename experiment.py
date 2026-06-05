import logging, logging.handlers
import datetime, time, socket, psutil


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
        return f"[ERROR] Connection refused"
    except socket.timeout:
        return f"[ERROR] TCP time out"
    except socket.gaierror:
        return "[ERROR] DNS ERROR"
    except Exception as e:
        return e
    finally:
        sock.close()


def network_monitor(network_targets):
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

        result = tcp_connection_reachable_check(addr, port, timeout_sec=1, ipv4=False)
        # print(f"{type} result: {result}")

        if result == "SUCCESS":
            logging.info(f"{type} connection to| host = {addr} | port = {port}| OK")

        else:
            logging.error(f"{type} connection to| host = {addr}| port = {port}| {result}")


if __name__ == "__main__":
    log_fname = "/Users/eleanor/git_local_repository/monitoring_agent/log/monitoring_agent.log"
    logging_setup(log_fname)

    network_targets = [{"type": "Internal", "addr": "2001:b000:168::2", "port": 53},
                       {"type": "Internal", "addr": "localhost", "port": 443},
                       {"type": "External", "addr": "www.graid.com", "port": 80},
                       {"type": "External", "addr": "7.7.7.7", "port": 22}]


    network_monitor(network_targets)
