from src.auto_getfile_from_gmail import job as gmail_job
from src.auto_job import main as gmail_schedule
from src.googledrive_operater import main as drive_main

def main():
    mode = ""
    while True:
        if mode == 0:
            break
        mode = input(
            "Input the number you want to do.\n"
            + "1: Use Gmail API\n"
            + "2: Use Gmail API every 5min\n"
            + "3: Use Drive API\n"
            + "0: Exit\n"
            + "Enter: "
        )
        mode = int(mode)
        if mode == 1:
            gmail_job()
        elif mode == 2:
            gmail_schedule()
        elif mode == 3:
            drive_main()
        else:
            pass

if __name__ == "__main__":
    main()