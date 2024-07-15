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
        return df.iloc[:-1]
    
    def get_orders(self):
        # display data on active orders on GBPUSD
        positions=mt5.positions_get(symbol=self.symbol)
        if positions==None:
            print("No positions on USDCHF, error code={}".format(mt5.last_error()))
        elif len(positions)>0:
            df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
            return df

    def close_order(self, order, ticket):
        if not order:
            print(f"No se encontró la orden con ticket {ticket}")
            mt5.shutdown()
            exit()

        # Preparar la solicitud de cierre
        order = order[0]
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order.symbol,
            "volume": order.volume,
            "type": mt5.ORDER_TYPE_SELL if order.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": ticket,
            "price": mt5.symbol_info_tick(order.symbol).bid if order.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(order.symbol).ask,
            "deviation": 20,
            "magic": 0,
            "comment": "Cierre de orden",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        # Enviar la solicitud de cierre
        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error al cerrar la orden: {result.retcode}")
        else:
            print("Orden cerrada exitosamente")


    def send_order(self, order_type):
        # prepare the buy request structure
        symbol = self.symbol
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()
            quit()
        
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol,True):
                print("symbol_select({}}) failed, exit",symbol)
                mt5.shutdown()
                quit()
        
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": self.lot,
            "type": mt5.ORDER_TYPE_SELL if order_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(self.symbol).bid if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(self.symbol).ask,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Envia una solicitud
        return mt5.order_send(request)


