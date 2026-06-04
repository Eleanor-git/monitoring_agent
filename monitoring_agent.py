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
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        if proc.info.get('status') == psutil.STATUS_ZOMBIE:
            zombies.append(proc.info)
    return zombies


if __name__ == "__main__":
    log_fname = "/Users/eleanor/git_local_repository/monitoring_agent/log/monitoring_agent.log"
    logging_setup(log_fname)
