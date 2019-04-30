import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from forex_python.converter import CurrencyRates



def CAD2USD(cad):
    c = CurrencyRates()
    return c.get_rate('CAD','USD') * cad


def USD2CAD(usd):
    return usd / CAD2USD(1)


def get_tickers(in_dict):
    '''Get list of tickers from a dictionary. Tickers must begin with capital 
    letters.'''
    tickers = np.array([t if t.isupper() else None for t in in_dict.keys()])
    return tickers[tickers != None]



def plot_timeseries_indiv(dataframe, quantity='frac_growth', pltt=True):
    plt.figure(figsize=(14,7))
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=5)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=5)
    
    #gain = dataframe[quantity] > dataframe[quantity][0]
    #loss = dataframe[quantity] <= dataframe[quantity][0]
    #ax1.plot(dataframe.index.map(mdates.date2num), dataframe[quantity], 'b-')
    #ax2.bar(dataframe.index.map(mdates.date2num), dataframe['volume'])
    
    ax1.plot(dataframe.index, dataframe[quantity], 'b-')
    ax2.bar(dataframe.index, dataframe['volume'])
    
    ax1.set_xticklabels('')
    ax1.set_ylabel(quantity, fontsize=12)
    ax1.set_title(dataframe['ticker'][0], fontsize=12)
    
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)

    if pltt:
        plt.show()
    plt.close('all')

    
    
    
def plot_timeseries_SP500(sp500_dict, ticker_dict={}, pltt=True):
    plt.figure(figsize=(14,7))
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=5)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=5)
   
    # plot sp500
    ax1.plot(sp500_dict['AAPL'].index, sp500_dict['sp500_frac_growth_mean'],
             'b-', label='mean S&P500')
    ax1.plot(sp500_dict['AAPL'].index, sp500_dict['sp500_frac_growth_median'],
             'g-', label='median S&P500')
    ax2.bar(sp500_dict['AAPL'].index, sp500_dict['sp500_volume'])
        
    # plot comparison ticker if given
    if len(ticker_dict) > 0:
        ticker = list(ticker_dict.keys())[0]
        ax1.plot(ticker_dict[ticker].index, ticker_dict[ticker]['frac_growth'],
                 'k-', label=ticker)
        
    ax1.set_xticklabels('')
    ax1.set_ylabel('S&P 500 fractional growth', fontsize=12)
    
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    
    ax1.legend(fontsize=12)

    if pltt:
        plt.show()
    plt.close('all')
