from re import I
import time
import pyupbit
import datetime
import numpy as np

access = "dNlYFPozFWnpa6gtT7OuOjLFbx7iD65qCkWVxxTg"
secret = "nzhg0ah7Lh3XX2nKlUxBY904RBoSbpBHMrf8pGrZ"
lis = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-AAVE","KRW-LTC","KRW-SOL","KRW-BSV","KRW-AVAX","KRW-AXS","KRW-STRK","KRW-BTG","KRW-ETC","KRW-ATOM","KRW-NEO","KRW-DOT","KRW-REP","KRW-LINK","KRW-WAVES","KRW-NEAR","KRW-QTUM","KRW-FLOW","KRW-WEMIX","KRW-GAS","KRW-SBD","KRW-OMG","KRW-TON","KRW-XTZ","KRW-SAND","KRW-KAVA","KRW-THETA","KRW-MANA","KRW-AQT","KRW-LSK","KRW-EOS","KRW-CBK","KRW-SRM","KRW-KNC","KRW-DAWN","KRW-MATIC","KRW-ENJ","KRW-1INCH","KRW-MTL","KRW-SXP","KRW-STX","KRW-BORA","KRW-STORJ","KRW-STRAX","KRW-ADA","KRW-PLA","KRW-HIVE","KRW-ALGO","KRW-ARK","KRW-MILK","KRW-ONG","KRW-IOTA","KRW-PUNDIX","KRW-XRP","KRW-BAT","KRW-HUNT","KRW-ICX","KRW-GRS","KRW-POWR","KRW-ONT","KRW-NU","KRW-CRO","KRW-GLM","KRW-POLY","KRW-ELF","KRW-STEEM","KRW-WAXP","KRW-CVC","KRW-HUM","KRW-HBAR","KRW-XLM","KRW-ARDR","KRW-AERGO","KRW-CHZ","KRW-TFUEL","KRW-MOC","KRW-DOGE","KRW-UPP","KRW-XEM","KRW-FCT2","KRW-DKA","KRW-STPT","KRW-LOOM","KRW-META","KRW-TRX","KRW-ORBS","KRW-ANKR","KRW-SNT","KRW-VET","KRW-JST","KRW-ZIL","KRW-SSX","KRW-MED","KRW-IOST"]
les = ["BTC","ETH","BCH","AAVE","LTC","SOL","BSV","AVAX","AXS","STRK","BTG","ETC","ATOM","NEO","DOT","REP","LINK","WAVES","NEAR","QTUM","FLOW","WEMIX","GAS","SBD","OMG","TON","XTZ","SAND","KAVA","KRW-THETA","MANA","AQT","LSK","EOS","CBK","SRM","KNC","DAWN","MATIC","ENJ","1INCH","MTL","SXP","STX","KRW-BORA","STORJ","STRAX","ADA","PLA","HIVE","ALGO","ARK","MILK","ONG","IOTA","PUNDIX","XRP","BAT","HUNT","ICX","GRS","POWR","ONT","NU","CRO","GLM","POLY","ELF","STEEM","WAXP","CVC","HUM","HBAR","XLM","ARDR","AERGO","CHZ","TFUEL","MOC","DOGE","UPP","XEM","FCT2","DKA","STPT","LOOM","META","TRX","ORBS","ANKR","SNT","VET","JST","ZIL","SSX","MED","IOST"]
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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
shift = 0
# 자동매매 시작
fin = []
while True:
    try: 
     for i in range(1,len(les)):
        now = datetime.datetime.now()
        coin = lis[i]
        coini = les[i]
        start_time = get_start_time(coin)
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            if shift == 0:
             target_price = get_target_price(coin,0.5)
             current_price = get_current_price(coin)
             if target_price < current_price:
              krw = get_balance("KRW")
              if coin not in fin: 
                if krw > 5000:
                 upbit.buy_market_order(coin, krw*0.9995)
                 shift = 1
                 print("풀매수 드가자!!!!!")
                 fin.append(coin)
                 buy_price = current_price
            if shift == 1:
               if current_price < buy_price * 0.97: 
                    upbit.sell_market_order(coin, btc*0.9995)
                    shift = 0   
               if current_price > buy_price * 1.20:
                    upbit.sell_market_order(coin, btc*0.9995)
                    shift = 0 
                    
        else:
            btc = get_balance(coini)
            upbit.sell_market_order(coin, btc*0.9995)
            shift = 0
            fin = []
        time.sleep(0.3)
    except Exception as e:
        print(e)
        
