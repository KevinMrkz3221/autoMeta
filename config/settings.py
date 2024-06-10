import os
from dotenv import load_dotenv
import argparse
import MetaTrader5 as mt5

from controllers.metaController import MetaController
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

META = MetaController(USER, PASSWORD, SERVER, TIMEFRAME, args.symbol, args.bars, args.lot)


# Crea directorio y files
try:
    os.mkdir('C:\\meta')
    os.mkdir('C:\\meta\\symbols\\')
    os.mkdir('C:\\meta\\logs\\')
except Exception as E:
    print(E)

FILE_HISTORY = f'C:\\meta\\symbols\\{args.symbol}.csv'
LOG_FILE = f'C:\\meta\\logs\\logs_{args.symbol}.csv'




# Historial de entradas
ENTRY = Entry(FILE_HISTORY)

# 
print(f'''
        Symbol: {args.symbol} Test
''')