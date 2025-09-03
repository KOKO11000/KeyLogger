from datetime import datetime
import os

DATA_DIR = "data"

def get_hourly_file_path(machine):
    now = datetime.now()
    hour_stamp = now.strftime("%Y%m%d_%H00")
    machine_dir = os.path.join(DATA_DIR, machine)
    os.makedirs(machine_dir, exist_ok=True)
    return os.path.join(machine_dir, f"{hour_stamp}.txt")


# חותמת זמן לשורה
def file_writer(machine, encrypted_data):
    filepath = get_hourly_file_path(machine)
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {encrypted_data}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(encrypted_data)