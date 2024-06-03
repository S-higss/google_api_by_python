import schedule, time, datetime, sys
from src.auto_getfile_from_gmail import job

def Schedule5minutes():
    # Calculate the time in the most recent 5 minute interval 
    current_minute = datetime.datetime.now().minute
    next_run_hour = datetime.datetime.now().hour
    next_run_minute = 5 * (current_minute // 5) + 5
    if next_run_minute >= 60:
        next_run_minute = next_run_minute - 60
        next_run_hour += 1
    return next_run_hour, next_run_minute

def main():
    print("Every 5min's schedules start at:")
    next_run_hour, next_run_minute = Schedule5minutes()
    print(f"{next_run_hour}:{next_run_minute:02}\n")
    # schedule.every().minutes.at(f":{next_run_minute:02}").do(job)
    for run_minutes in range(12):
        next_run = run_minutes * 5
        schedule.every().hour.at(f":{next_run:02}").do(job_func=job)

    # Schedule next run
    while True:
        try:
            schedule.run_pending()
            sys.stdout.flush()
            time.sleep(22)
        except KeyboardInterrupt:
            # if press Ctrl+C, terminate the program
            break

if __name__ == "__main__":
    job()