import os
from dotenv import load_dotenv
import argparse
import MetaTrader5 as mt5


from controllers.metaController import MetaController
from controllers.tradeLogController import TradeLogController
from controllers.positionController import PositionController
from models.entry import Entry

load_dotenv()



# Configuracion de argumentos 
parser = argparse.ArgumentParser(description="AutoMeta")
parser.add_argument(
    '--symbol', '-s', type=str, 
    help="Símbolo del par de divisas a operar. Ejemplo: --symbol EURUSD o -s EURUSD"
)

parser.add_argument(
    '--timeframe', '-t', type=str, choices=['1M', '5M', '10M', '15M', '30M', '1H', '2H', '4H', '12H', '1D'],
    help="Seleccione el marco temporal: 1M, 5M, 10M, 15M, 30M, 1H, 2H, 4H, 12H, 1D"
)

parser.add_argument(
    '--bars', '-b', type=int, 
    help="Número de barras de historial a recuperar. Ejemplo: --bars 400 o -b 400"
)

# Agregar el argumento `--lot`
parser.add_argument(
    '--lot', '-l', type=float, 
    help="Tamaño del lote para la operación. Ejemplo: --lot 0.01 o -l 0.01"
)

# Agregar el argumento `--strategy`
parser.add_argument( '--strategy', '-st', type=str, help="Agrega la estrategia. Ejemplo: -s volatility")
# Parsea los argumentos de la línea de comandos
args = parser.parse_args()


# Seleccion de timeframe

if args.timeframe == '1M':
    TIMEFRAME = mt5.TIMEFRAME_M1
elif args.timeframe == '5M':
    TIMEFRAME = mt5.TIMEFRAME_5M
elif args.timeframe == '10M':
    TIMEFRAME = mt5.TIMEFRAME_M10
elif args.timeframe == '15M':
    TIMEFRAME = mt5.TIMEFRAME_M15
elif args.timeframe == '30M':
    TIMEFRAME = mt5.TIMEFRAME_M30
elif args.timeframe == '1H':
    TIMEFRAME = mt5.TIMEFRAME_H1
elif args.timeframe == '2H':
    TIMEFRAME = mt5.TIMEFRAME_H2
elif args.timeframe == '4H':
    TIMEFRAME = mt5.TIMEFRAME_H4
elif args.timeframe == '12H':
    TIMEFRAME = mt5.TIMEFRAME_H12
elif args.timeframe == '1D':
    TIMEFRAME = mt5.TIMEFRAME_D1


# USER CREDENTIALS
USER = int(os.getenv('USER'))
PASSWORD = os.getenv('PASSWORD')
SERVER = os.getenv("SERVER")




# Crea directorio y files
try:
    os.mkdir('C:\\meta')
except Exception as E:
    print(E)

try:
    os.mkdir(f'C:\\meta\\{args.strategy}\\')
except Exception as E:
    print(E)

try:
    os.mkdir(f'C:\\meta\\{args.strategy}\\{args.symbol}\\')
except Exception as E:
    print(E)

# Archivos para historicos
LOG_FILE = f'C:\\meta\\{args.strategy}\\{args.symbol}\\logs_{args.symbol}.csv'

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as logfile:
        logfile.write('entry_time,exit_time,entry_price,exit_price,signal,lot\n')
        logfile.close()


# Controladores
# Controlador de meta
META = MetaController(USER, PASSWORD, SERVER, TIMEFRAME, args.symbol, args.bars, args.lot)
# Log Controller se encarga de llenar el archivo de logs sera un CREATE, READ
LOG_CONTROLLER = TradeLogController(LOG_FILE)

# Lee las posiciones abiertas se va a encargar de llenar
# y eliminar registros dentro del archivo de posiciones
POSITION_CONTROLLER = PositionController()

POSITION_CONTROLLER.get_positions(META.get_orders())

# 
print(f'''
        Symbol: {args.symbol} Test
''')

