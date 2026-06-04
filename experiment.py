import psutil

def get_zombie_processes():
    zombies = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        if proc.info.get('status') == psutil.STATUS_ZOMBIE:
            zombies.append(proc.info)
    return zombies

lst_info = get_zombie_processes()

print(lst_info)

