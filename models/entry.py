from datetime import datetime
import os

class Entry:
    def __init__(self, filename):
        self.filename = filename
        
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("date,action,symbol,volume,type,price,sl,tp,type_time,type_filling,deviation,magic,comment\n")


        

    def add_record(self, text):
        with open(self.filename, "a") as f:
            f.write(f"{datetime.now()}, {text} \n")
