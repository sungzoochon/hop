from re import I
import time
import pyupbit
import datetime
import numpy as np

access = "your code"
secret = "your code"
lis = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-AAVE","KRW-LTC","KRW-SOL","KRW-BSV","KRW-AVAX","KRW-AXS","KRW-STRK","KRW-BTG","KRW-ETC","KRW-ATOM","KRW-NEO","KRW-DOT","KRW-REP","KRW-LINK"]
les = ["BTC","ETH","BCH","AAVE","LTC","SOL","BSV","AVAX","AXS","STRK","BTG","ETC","ATOM","NEO","DOT","REP","LINK"]
def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC")
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def   get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None: 
                return float(b['balance'])
            else:
                return 0
    return 0
  
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_avg_buy_price(ticker):
    """매수평균가 조회"""
    sdf = pyupbit.get_avg_buy_price(ticker)
    return sdf
# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
shift = 0
# 자동매매 시작
while True:
    try: 
      for i in range(1,18):
        if shift == 0:
         coin = lis[i]
         coini = les[i]
        now = datetime.datetime.now()
        start_time = get_start_time(coin)
        end_time = start_time + datetime.timedelta(days=1)
        m = 0
        res = 0
        for k in np.arange(0.1, 1.0, 0.1):
          ror = get_ror(k)
          if ror > m:
              m = ror
              res = k
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            res = round(res,1)  
            
            target_price = get_target_price(coin, res)
            current_price = get_current_price(coin)
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(coin, krw)
                    shift = 1
                    print("풀매수 드가자!!!!!")
                    buy_price = current_price
            if shift == 1:
               
               if current_price < buy_price * 0.97: 
                    upbit.sell_market_order(coin, btc)
                    shift = 0
                    print("하락이다 돔황차!!!!!")
               
        else:
            btc = get_balance(coini)
            upbit.sell_market_order(coin, btc)
            shift = 0
            print("다들 돔황차!!!!!")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
