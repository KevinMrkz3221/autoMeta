from strategy.trends import signal
from config.settings import META, args, ENTRY, mt5
from models.request import Request
from datetime import datetime

def made_request():
    pass

def run():
    data = META.get_data()
    
    _signal = signal(data, args.bars)

    if _signal == None:
        req = None

    elif _signal == 1:
        req = Request(
            action=mt5.TRADE_ACTION_DEAL,
            symbol=META.symbol,
            volume=META.lot,
            _type=mt5.ORDER_TYPE_SELL,
            price=mt5.symbol_info_tick(META.symbol).ask,
            sl=0,
            tp=0,
            _type_time=mt5.ORDER_TIME_GTC,
            type_filling=mt5.ORDER_FILLING_IOC
        )

    elif _signal == 0:
        req = Request(
            action=mt5.TRADE_ACTION_DEAL,
            symbol=META.symbol,
            volume=META.lot,
            _type=mt5.ORDER_TYPE_BUY,
            price=mt5.symbol_info_tick(META.symbol).ask,
            sl=0,
            tp=0,
            _type_time=mt5.ORDER_TIME_GTC,
            type_filling=mt5.ORDER_FILLING_IOC
        )

    print(req, str(data.tail(1).to_dict('records')[0]['time']))
    # Verifica si el request no es nulo
    if req != None:
        request = META.send_order(req.to_dict())
        print(request)
        ENTRY.add_record(data.tail(1).to_dict('records'))

        
        

        