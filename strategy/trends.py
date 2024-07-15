from scipy.signal import find_peaks
import numpy as np
from scipy import stats


def find_peaks_valleys(df):
    ## 100 works fine on EURUSD
    peaks, _ = find_peaks(df['close'], distance=100)
    valleys, _ = find_peaks(-df['close'], distance=100)

    return peaks, valleys


# Función para calcular la línea de tendencia en una ventana de datos
def calculate_trend(data, start_idx, window_size):
    # Limitar el índice para evitar errores de índice negativo

    start = max(start_idx - window_size, 0)
    end = start_idx + 1
    # Regresión lineal para la ventana de datos
    x = np.arange(start, end)
    y = data[start:end]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept

def find_trends(points, df, window_size):
    trends = []
    for point in points:
        slope, intercept = calculate_trend(df['close'], point, window_size)
        trends.append({'peak': point, 'slope': slope, 'intercept': intercept})

    return trends

def trigger(df, peak_trends, valley_trends):
    # print( f'Peak {peaks[-1]}, valley {valleys[-1]}')
    # Si el indice de peak es mayor que el de valley tenemos una venta
    # Entonces nuestra pendiente tienee que ser menor a cero para disparar la venta
    if peak_trends[-1]['peak'] > valley_trends[-1]['peak']:
        if peak_trends[-1]['slope'] < 0 and df.index[-2] == peak_trends[-1]['peak']:
            return 1
    # Si el indice valley es mayor tenemos una compra
    # Entonces nuestra pendiente tiene que ser positiva para disparar una compra
    elif valley_trends[-1]['peak'] > peak_trends[-1]['peak']:
        if  valley_trends[-1]['slope'] > 0 and df.index[-2] == valley_trends[-1]['peak']:
            return 0


# Envia la señal
def signal(df, window_size):
    peaks, valleys = find_peaks_valleys(df)
    peak_trends = find_trends(peaks, df, window_size)
    valley_trends = find_trends(valleys, df, window_size)

    signal = trigger(df, peak_trends, valley_trends)


    return signal