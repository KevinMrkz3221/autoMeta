from dataclasses import dataclass
import datetime

@dataclass
class Position:
    ticket: str    
    time: datetime
    _type: int
    magic: int
    identifier: int
    reason: int
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float
    profit: float
    symbol: str
    comment: str



    def to_dict(self):
        return {
            'ticket': self.ticket,    
            'time': self.time,
            '_type': self._type,
            'magic': self.magic,
            'identifier': self.identifier,
            'reason': self.reason,
            'volume': self.volume,
            'price_open': self.price_open,
            'sl': self.sl,
            'tp': self.tp,
            'price_current': self.price_current,
            'swap': self.swap,
            'profit': self.profit,
            'symbol': self.symbol,
            'comment': self.comment
        }


