import time
import pyupbit
import datetime
import numpy as np

access = "dNlYFPozFWnpa6gtT7OuOjLFbx7iD65qCkWVxxTg"
secret = "nzhg0ah7Lh3XX2nKlUxBY904RBoSbpBHMrf8pGrZ"
les = ["BTC","ETH","BCH","AAVE","LTC","SOL","BSV","AVAX","AXS","STRK","BTG","ETC","ATOM","NEO","DOT","REP","LINK","WAVES","NEAR","QTUM","FLOW","WEMIX","GAS","SBD","OMG","TON","XTZ","SAND","KAVA","KRW-THETA","MANA","AQT","LSK","EOS","CBK","SRM","KNC","DAWN","MATIC","ENJ","1INCH","MTL","SXP","STX","KRW-BORA","STORJ","STRAX","ADA","PLA","HIVE","ALGO","ARK","MILK","ONG","IOTA","PUNDIX","XRP","BAT","HUNT","ICX","GRS","POWR","ONT","NU","CRO","GLM","POLY","ELF","STEEM","WAXP","CVC","HUM","HBAR","XLM","ARDR","AERGO","CHZ","TFUEL","MOC","DOGE","UPP","XEM","FCT2","DKA","STPT","LOOM","META","TRX","ORBS","ANKR","SNT","VET","JST","ZIL","SSX","MED","IOST"]
def get_ror(k=0.5,coin = "KRW-BTC"):
    df = pyupbit.get_ohlcv(coin, count=4)
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

def get_balance(ticker):
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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
coin = ""
coini = ""
shift = 1
buylist = []
res = 0
buyprice = 0
i = len(les) - 1
while True:
    try:
     if i >= 0:    
         now = datetime.datetime.now()
         if shift == 0:
          coin = "KRW-"+les[i]
          coini = les[i]
         start_time = get_start_time(coin)
         end_time = start_time + datetime.timedelta(days=1)
         if start_time < now < end_time - datetime.timedelta(seconds=5):
            if shift == 0:
             ror = []   
             for k in np.arange(0.1, 1.0, 0.1):
              ror.append(get_ror(k,coin))
             M = max(ror)
             res = (ror.index(M) + 1)/10
             print(res,coin) 
             target_price = get_target_price(coin,res)
             current_price = get_current_price(coin)
             if coin not in buylist:   
              if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(coin, krw*0.9995)
                    shift = 1
                    buylist.append(coin)
                    buy_price = current_price
                    print("상승이다 풀매수!!!!")
            if shift == 1:
             if buy_price*0.955 > current_price:
                btc = get_balance(coini)
                upbit.sell_market_order(coin, btc)
                print("하락장이다 돔황차!!!!")
             if buy_price*1.15 < current_price:
                btc = get_balance(coini)
                upbit.sell_market_order(coin, btc)
                print("익절이다 돔황차!!!!")
         else:
            btc = get_balance(coini)
            if btc > 0.00008:
                upbit.sell_market_order(coin, btc)
                shift = 0
                buylist = []
                print("9시다 돔황차!!!!") 
         i = i - 1   
     else:
         i = len(les) - 1      
    except Exception as e:
        pass
