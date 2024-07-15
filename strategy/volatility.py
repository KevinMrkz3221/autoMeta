import pandas as pd
import numpy as np
from config.settings import args, LOG_CONTROLLER, POSITION_CONTROLLER, META
import MetaTrader5 as mt5

def signal():
    df = META.get_data()
    historical_data = df.copy()[:-1]
    current_row = df.iloc[-1]
    # Calcular el log_return
    historical_data.loc[:, 'log_return'] = np.log(historical_data['close'] / historical_data['close'].shift(1))

    # Calcular historical_volatility
    historical_data.loc[:, 'historical_volatility'] = historical_data['log_return'].rolling(window=21).std() * np.sqrt(252)
    historical_data.dropna(inplace=True)

    # Obtener la volatilidad histórica del último registro en la ventana deslizante
    historical_volatility = historical_data['historical_volatility'].iloc[-1]
    
    # Definir umbrales de volatilidad dinámicamente
    low_volatility_threshold = historical_data['historical_volatility'].quantile(0.2)
    high_volatility_threshold = historical_data['historical_volatility'].quantile(0.8)

    # Verificar señales de compra/venta en base a la volatilidad de la fila actual
    current_volatility = historical_volatility


    if current_volatility < low_volatility_threshold:
        signal = 0
        META.send_order(signal)

        POSITION_CONTROLLER.get_positions(META.get_orders())
        print(f'{current_row['time']} - Se ejecuto una compra')

    elif current_volatility > high_volatility_threshold:
        signal = 1
        META.send_order(signal)
        POSITION_CONTROLLER.get_positions(META.get_orders())
        print(f'{current_row['time']} - Se ejecuto una venta')

    else:
        print(f'{current_row['time']} - No se ejecuto ninguna operacion')


    # Verificar si hay posiciones abiertas y evaluar condiciones de cierre
    for position in POSITION_CONTROLLER.positions:
        if position.to_dict()['_type'] == 0 and current_row['close'] > position.to_dict()['price_open']:
            exit_price = current_row['close']
            exit_time = current_row['time']

            LOG_CONTROLLER.add_log({
                'entry_time': position.to_dict()['time'], 
                'exit_time': exit_time, 
                'entry_price': position.to_dict()['price_open'], 
                'exit_price': exit_price, 
                'signal': position.to_dict()['_type'], 
                'units': position.to_dict()['volume'], 

            })
            # POSITION_CONTROLLER.positions.remove(position)
            ticket = position.to_dict()['ticket']
            order = mt5.positions_get(ticket=ticket)
            META.close_order(order, ticket)
            POSITION_CONTROLLER.get_positions(META.get_orders())

        elif position.to_dict()['_type'] == 0 and current_row['close'] < position.to_dict()['price_open']:
            exit_price = current_row['close']
            exit_time = current_row['time']

            LOG_CONTROLLER.add_log({
                'entry_time': position.to_dict()['time'], 
                'exit_time': exit_time, 
                'entry_price': position.to_dict()['price_open'], 
                'exit_price': exit_price, 
                'signal': position.to_dict()['_type'], 
                'units': position.to_dict()['volume']
            })

            ticket = position.to_dict()['ticket']
            order = mt5.positions_get(ticket=ticket)   
            META.close_order(order, ticket)
            POSITION_CONTROLLER.get_positions(META.get_orders())