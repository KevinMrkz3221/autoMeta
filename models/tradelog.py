from dataclasses import dataclass
import datetime

@dataclass
class TradeLog:
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    signal: str
    lot: float

    

    def to_dict(self):
        return {
            'entry_time': self.entry_time,
            'exit_time': self.exit_price,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'signal': self.signal,
            'lot': self.lot
        }