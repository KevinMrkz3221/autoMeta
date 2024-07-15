import pandas as pd
from models.position import Position

## Este metodo no guardara datos historicos de las entradas
## El responsable de esto sera el TradeLogController
class PositionController:
    ## Metodo read
    def get_positions(self, df):
        self.positions = []
        try: 
            records = df.to_dict('records')
        except:
            pass
        try:
            # Llenar la lista de posiciones abiertas
            for data in records:
                self.positions.append(
                    Position(
                        data['ticket'],
                        data['time'],
                        data['type'],
                        data['magic'],
                        data['identifier'],
                        data['reason'],
                        data['volume'],
                        data['price_open'],
                        data['sl'],
                        data['tp'],
                        data['price_current'],
                        data['swap'],
                        data['profit'],
                        data['symbol'],
                        data['comment']
                    )
                )
            
        except Exception as E:
            pass
        
