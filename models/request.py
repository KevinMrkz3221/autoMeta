from dataclasses import dataclass

@dataclass
class Request:
    action: int
    symbol: str
    volume: float
    _type:  int
    price: float
    sl: float
    tp: float
    _type_time: int
    type_filling: int
    deviation: int = 20
    magic: int = 234000
    comment: str = "Python Script Open"
    

    def to_line(self):
        return f"{self.action},{self.symbol},{self.volume},{self._type},{self.price},{self.sl},{self.tp},{self._type_time},{self.type_filling},{self.deviation},{self.magic}, {self.comment}"

    def to_dict(self):

        return {
            "action": self.action,
            "symbol": self.symbol,
            'volume': self.volume,
            "type": self._type,
            'price': self.price,
            'deviation': self.deviation,
            'magic': self.magic,
            'comment': self.comment,
            'type_time': self._type_time,
            'type_filling': self.type_filling
        }
