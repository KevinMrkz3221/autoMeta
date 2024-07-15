from config.src import run
import schedule
import time
from datetime import datetime 

def job():
    current_minute = datetime.now().minute
    current_second = datetime.now().second
    seconds_to_wait = (60 - current_minute) * 60 - current_second
    time.sleep(seconds_to_wait)
    run()
    schedule.every().hour.at(":00").do(run)

if __name__ == '__main__':
    job()  # Ejecuta la función run() al inicio de la siguiente hora
    while True:
        schedule.run_pending()
        time.sleep(1)
