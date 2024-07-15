from config.settings import  args
from strategy.volatility import signal

def volatility_strategy():
    signal()


def run():
    
    if args.strategy == 'volatility':
        volatility_strategy()
    else:
        print(f'La estrategia {args.strategy} no esta permitida')
        
        

        