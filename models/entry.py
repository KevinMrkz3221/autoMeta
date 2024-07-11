from datetime import datetime
import os

class Entry:
    def __init__(self, filename):
        self.filename = filename
        
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("date,action,symbol,volume,type,price,sl,tp\n")

    def add_record(self, text):
        record = ''
        print(list(text[0].keys()))
        datet = text[0]['time']
        for key in list(text[0].keys())[1:]:
            record = record  + str(text[0][key]) + ','
        with open(self.filename, "a") as f:
            f.write(f"{datet}, {record} \n")
