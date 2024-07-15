import pandas as pd
from models.tradelog import TradeLog


class TradeLogController:
    def __init__(self, file) -> None:
        self.file = file   


    def get_current_logs(self):
        # Esto sera un listado de TradeLog
        logs = []
        records = pd.read_csv(self.file).to_dict('records')

        for record in records:
            logs.append(TradeLog(
                record['entry_time'],
                record['exit_time'],
                record['entry_price'],
                record['exit_price'],
                record['signal'],
                record['lot']
            ))

        return logs

    def add_log(self, new_log):
        logs = self.get_current_logs()
        new = TradeLog(
                new_log['entry_time'],
                new_log['exit_time'],
                new_log['entry_price'],
                new_log['exit_price'],
                new_log['signal'],
                new_log['units']
            )
        logs.append(new)

        # Se manda a llamar write logs
        self.write_logs(logs)


    def write_logs(self, logs):
        records = [log.to_dict() for log in logs]
        pd.DataFrame.from_records(records).to_csv(self.file, index=False)
