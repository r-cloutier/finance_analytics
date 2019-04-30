import numpy as np
import matplotlib.dates as mdates
from yahoo_fin import stock_info as si
import datetime as dt
import pickle, os


def get_sp500_timeseries(start_date, end_date, retrieve_new_data=False):
    '''Get the time series data of all S&P500 tickers over an input date range.'''

    # save s&p500 ticker data to a dictionary if necessary or updated data is
    # desired
    sp500_ticker_fname = './sp500_ticker_data_%s_%s'%(start_date.isoformat(), 
						      end_date.isoformat())
    if not os.path.exists(sp500_ticker_fname) or retrieve_new_data:
        sp500_dict, count = {}, 0
        
        # skip first entry which is a header
        for t in np.sort(si.tickers_sp500()[1:]):

            count += 1
            print('%.3d\t%s'%(count, t))

            try:
                sp500_dict[t] = si.get_data(t, start_date=start_date,
                                            end_date=end_date)
            except KeyError:
                pass
                
        # pickle the ticker data
        f = open(sp500_ticker_fname, 'wb')
        pickle.dump(sp500_dict, f)
        f.close()
    
    
    # read-in ticker data if it exists and no override is insisted upon
    else:
        f = open(sp500_ticker_fname, 'rb')
        sp500_dict = pickle.load(f)
        f.close()
        
        # restrict date range if they do not already match
        if (sp500_dict['AAPL'].index[0] < start_date.date()) | \
           (sp500_dict['AAPL'].index[-1] > end_date.date()):
            print('Restricting to the new date range of %s to %s.'%(start_date.isoformat(), end_date.isoformat()))
            for t,df in sp500_dict.items():
                sp500_dict[t] = df.loc[start_date.date() : end_date.date()]
                
            # pickle the ticker data over the new date range
            f = open(sp500_ticker_fname, 'wb')
            pickle.dump(sp500_dict, f)
            f.close()
    
    # return dicitionary of sp500 tickers and their available time series
    return sp500_dict



def compute_fractional_growth(ticker_dict, quantity='adjclose'):
    '''Given a dictionary of ticker keys and time series data values, compute the fractional growth of each ticker
    over time which is set by the doctionary data.'''
    for t, df in ticker_dict.items():
        
        # ensure that this quantity has time series data
        try:
            arr = df[quantity]
        except KeyError:
            raise ValueError('Input time series quantity must one of: "%s".'%('", "'.join(df.columns)))
        
        # compute the fractional growth of this quantity from the initial epoch
        ticker_dict[t]['frac_growth'] = (arr - arr[0]) / arr[0]
        
    # return dictionary of tickers and their time series including their
    # fractional growth
    return ticker_dict


def compute_sp500_fractional_growth(sp500_ticker_dict):
    '''Ad hoc calculation of the fractional growth of the S&P500 index from a
    dictionary of all sp500 ticker fractional growth time series.'''
    # compile fractional growth time series
    Ntickers = len(sp500_ticker_dict)
    Npnts,_ = sp500_ticker_dict['AAPL'].shape
    sp500_fractional_growth = np.zeros((Npnts,Ntickers))
    sp500_volume = np.zeros((Npnts,Ntickers))
    i = 0 
    for t, df in sp500_ticker_dict.items():
        
        if df['frac_growth'].size == Npnts:
            sp500_fractional_growth[:,i] = df['frac_growth'] 
            sp500_volume[:,i] = df['volume']
            
        else:
            sp500_fractional_growth[:,i] = np.repeat(np.nan,Npnts)
            sp500_volume[:,i] = np.repeat(np.nan,Npnts)

        i += 1

    # compute average fractional growth of the sp500
    sp500_ticker_dict['sp500_frac_growth_mean'] = \
                                np.nanmean(sp500_fractional_growth, axis=1) 
    sp500_ticker_dict['sp500_frac_growth_median'] = \
                                np.nanmedian(sp500_fractional_growth, axis=1) 

    # add sp500 volume
    sp500_ticker_dict['sp500_volume'] = np.nansum(sp500_volume, axis=1)
    
    # compute change in time
    tarr = sp500_ticker_dict['AAPL'].index.map(mdates.date2num)
    sp500_ticker_dict['delta_t_days'] = tarr - tarr.min()
    
    return sp500_ticker_dict
