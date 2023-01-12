from datetime import datetime


def generate_time_id() -> str:
    now = datetime.now()
    time_id = now.strftime("%y%m%d%H%M")
    return time_id
