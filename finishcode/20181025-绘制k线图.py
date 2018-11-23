import tushare as ts
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
data = ts.get_k_data('603026', ktype='D', autype='qfq', start='2017-09-17', end='')
prices = data[['open', 'high', 'low', 'close']]
dates = data['date']
candleData = np.column_stack([list(range(len(dates))), prices])
fig = plt.figure(figsize=(10, 6))
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
mpf.candlestick_ohlc(ax, andf[1:], width=0.5, colorup='r', colordown='b')
plt.show()





middata[(middata.date>='2018-10-29 18:09:00') & (middata.date<='2018-10-29 18:10:00')]
a=middata[(middata.date>=index[i+1]) & (middata.date<index[i])]