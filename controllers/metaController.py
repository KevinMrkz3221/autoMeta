from dataclasses import dataclass
import pandas as pd
from config.settings import mt5

@dataclass
class MetaController:
    usr: int
    password: str
    server: str
    timeframe: int
    symbol: str
    num_bars: int
    lot: float

    def __post_init__(self):
        # Intentar inicializar MetaTrader 5
        if not mt5.initialize(login=self.usr, password=self.password, server=self.server):
            raise RuntimeError(f"Error al inicializar MetaTrader 5: {mt5.last_error()}")
        

    def get_data(self):
        # Obtiene las ultimas n velas
        bars = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, self.num_bars)
        # Convierte a df
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['candle_number'] = list(range(1, len(df) + 1))
        return df

    def send_order(self, request):
        # Envia una solicitud
        return mt5.order_send(request)


