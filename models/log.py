from datetime import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.add_log('Start')

    def add_log(self, text):
        with open(self.filename, "a") as f:
            f.write(f"EXECUTION: {datetime.now()} | {text} \n")
