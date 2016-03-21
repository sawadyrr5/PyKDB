from PyKDB import PyKDB as kdb
from datetime import datetime

myKDB = kdb()
#    u_symbol = 'F101-1606'  #future
#    u_symbol = 'I101'       #index
#     u_symbol = '9984-T'      #stock
u_symbol = 'T1'         #stat

# daily sample
d_start = datetime(2014,  3, 14)
d_end   = datetime(2015,  3, 20)
df = myKDB.hist(u_symbol, 'd', d_start, d_end)
print(df)

# minutely sample
d_date  = datetime(2016,  3, 18)
df = myKDB.hist(u_symbol, 'm', d_date, None)
print(df)


ohlc_dict = {
    'Open':'first',
    'High':'max',
    'Low':'min',
    'Close': 'last',
    'Volume': 'sum',
    'DollarVolume': 'sum'
}
s_df = df.resample('3T', how=ohlc_dict, closed='right', label='right', kind='Period')
print(s_df)