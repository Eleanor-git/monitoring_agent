import os
import time

def create_zombie():
    # 建立子進程
    pid = os.fork()

    if pid > 0:
        # 父進程分支
        print(f"[父進程] 我的 PID 是 {os.getpid()}，子進程 PID 是 {pid}")
        print("[父進程] 我將休眠 30 秒，期間不處理子進程的狀態。")
        print("[父進程] 請在此期間打開另一個終端機觀察殭屍進程（狀態為 Z）。")
        time.sleep(30)
        print("[父進程] 結束，此時系統會自動將殭屍進程託管給 init/systemd 並被清理。")
    
    elif pid == 0:
        # 子進程分支
        print(f"[子進程] 我的 PID 是 {os.getpid()}，我即將立刻結束並變成殭屍...")
        # 子進程立刻退出，但父進程還在 sleep，沒調用 wait()，此時子進程變成殭屍
        os._exit(0)

if __name__ == "__main__":
    create_zombie()
