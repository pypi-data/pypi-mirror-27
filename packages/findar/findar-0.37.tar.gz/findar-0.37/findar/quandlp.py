import quandl
import time
from .google import *

# attribute is for HK stocks only, can be either 'unadj_close' or 'simple_ret'


def quandlPrice(tics=[], mkt='US', year=3,
                begdate='', enddate='', APIkey=''):
    quandl.ApiConfig.api_key = APIkey
    if (enddate == ''):
        enddate = datetime.now()
        begdate = enddate - relativedelta(years=year)
    else:
        enddate = datetime.strptime(str(enddate), '%Y%m%d')
        begdate = datetime.strptime(str(begdate), '%Y%m%d')

    enddate = enddate.strftime("%Y-%m-%d")
    begdate = begdate.strftime("%Y-%m-%d")

    count = 0
    while True:
        try:
            count += 1
            if (mkt == 'US' or mkt == 'us'):
                print("Getting data from quandl:WIKI/PRICES")
                df = quandl_us(tics, begdate, enddate)
            elif(mkt == 'HK' or mkt == 'hk'):
                print("Getting data from quandl:HKEX")
                dfa = quandl.get(['HKEX/%s.1' % (x) for x in tics],
                                 start_date=begdate, end_date=enddate)
                dfa = dfa / dfa.shift(1) - 1  # convert to simple return
                dfa = dfa.fillna(0)
                dfb = quandl.get(['HKEX/%s.12' % (x) for x in tics],
                                 start_date=begdate, end_date=enddate)
                df = pd.concat([dfa, dfb], axis=1)
                df = df.iloc[1:]
                df.columns = [['%s.HK_ret' % x for x in tics] +
                              ['%s.HK_boardlot' % x for x in tics]]

            else:
                print('Market must be US or HK.')
                return
            break
        except Exception:
            if count >= 5:
                print('Network Err')
                return
            else:
                time.sleep(1 * count)
                continue
    print('quandlPrice successful')
    return df


def quandl_us(tics, begdate, enddate):
    data = []
    df = pd.DataFrame()
    tasks = [x * 50 for x in range(len(tics) / 50 + 1)] + [len(tics)]
    for i in range(1, len(tasks)):
        print('Getting chunk %s ' % i)
        d = quandl.get_table('WIKI/PRICES',
                             qopts={'columns': [
                                    'ticker', 'date', 'adj_close']},
                             ticker=tics[tasks[i - 1]: tasks[i]],
                             date={'gte': begdate,
                                   'lte': enddate},
                             paginate=True)
        gpt = d.groupby('ticker')
        for ticker, df in gpt:
            df = df.set_index('date').drop('ticker', axis=1)
            df.columns = [ticker]
            data.append(df)
    if data:
        df = pd.concat(data, axis=1)
    return df


def HKPrice_formatter(df):
    cols = df.columns.to_series()
    tickers = [x[:-4] for x in cols][:(len(cols)) / 2]
    dfa = df[df.columns[cols.str.contains('_ret')]]
    dfa.columns = tickers
    return dfa


def HKBoardLot_formatter(df):
    cols = df.columns.to_series()
    tickers = [x[:-4] for x in cols][:(len(cols)) / 2]
    dfb = df[df.columns[cols.str.contains('_boardlot')]]
    dfb.columns = tickers
    dfb = dfb.fillna(method='ffill').iloc[-1]
    dfb = dfb.fillna(-999).astype(int)
    dfb = pd.DataFrame(dfb)
    dfb.columns = ['Board_Lot']
    return dfb


if __name__ == '__main__':
    from .datareader import *
    tics1 = getCons('SP500').iloc[:, 0].values.tolist()
    tics2 = getCons('HSI').iloc[:, 0].values.tolist()

    df1 = quandlPrice(tics1, mkt='US')
    df2 = quandlPrice(tics2, mkt='HK')
