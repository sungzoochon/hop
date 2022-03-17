import time
import pyupbit
import datetime
import numpy as np
access = "dNlYFPozFWnpa6gtT7OuOjLFbx7iD65qCkWVxxTg"
secret = "nzhg0ah7Lh3XX2nKlUxBY904RBoSbpBHMrf8pGrZ"
les = ["BTC","ETH","BCH","AAVE","LTC","SOL","BSV","AVAX","AXS","STRK","BTG","ETC","ATOM","NEO","DOT","REP","LINK","WAVES","NEAR","QTUM","FLOW","WEMIX","GAS","SBD","OMG","TON","XTZ","SAND","KAVA","THETA","MANA","AQT","LSK","EOS","CBK","SRM","KNC"]

def get_ror(k=0.5,coin = "KRW-BTC"):
  try:
    df = pyupbit.get_ohlcv(coin, count=3)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range']

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)
    ror = df['ror'].cumprod()[-2]
    return ror
  except Exception as e:
        return "error"
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
def get_K(coin):
    """K값을 구하는 코드"""
    ror = []
    for k in np.arange(0.1, 1.0, 0.1):
     temporary = get_ror(k,coin)
     if temporary == "error":
      k = k - 0.1
      continue
     else:
      ror.append(temporary)
    m = max(ror)
    res = (ror.index(m) + 1)/10
    return res
upbit = pyupbit.Upbit(access, secret)
coini ="BTC"
coin = "KRW-"+ coini 
res = 0
buy_price =[6845,0]
ror = []
res = 0 
buy_list = ["FLOW",""]
bought_list = []
asd = 0
i = 0
target_list = [0 for i in range(len(les))] 
print("나도 부자 될꺼다") 
while True:
 try:
  start_time = get_start_time(coin)
  end_time = start_time + datetime.timedelta(days=1)- datetime.timedelta(minutes=2)
  break
 except Exception as e:
  continue
while True:
    try:
     if i < len(les):
         time.sleep(0.1)    
         now = datetime.datetime.now()
         coini = les[i]
         coin = "KRW-"+les[i]
         if start_time < now < end_time:
            if asd == 1:
              time.sleep(1)
              asd = 0
            if buy_price.count(0) != 0 and get_balance("KRW") > 5000:
             if coini not in bought_list:
              current_price = get_current_price(coin)
              if target_list[i] == 0:
                target_list[i] = get_target_price(coin,0.3)
              print(coin, current_price, target_list[i])
              if target_list[i] < current_price <= target_list[i] * 1.0045:          
                money = get_balance("KRW")/buy_price.count(0)
                upbit.buy_market_order(coin, money * 0.9995)
                for i in range(0,2):
                 if buy_list[i] == "":
                  buy_list[i] = coini
                  buy_price[i] = current_price
                  break
                 else:
                  continue
                print(coin,current_price,"원에 존버")
                bought_list.append(coini)
                if buy_price.count(0) == 0:
                  print(buy_list[0],buy_list[1],"분할매수 완료")
                  print("제발 제발 떡상 가자 제발 부탁이다")
            for n in range(0,2):
              if buy_list[n] != "" and buy_price[n] != 0:   
               current_price = get_current_price("KRW-"+buy_list[n])
               if buy_price[n] * 0.95 > current_price:
                btc = get_balance(buy_list[n])
                upbit.sell_market_order("KRW-"+buy_list[n], btc)
                print(buy_list[n],"손절 돔황차!!!!")
                buy_list[n] = ""
                buy_price[n] = 0
               #if buy_price[n] * 2 < current_price:
                #btc = get_balance(buy_list[n])one is
                #upbit.sell_market_order("KRW-"+buy_list[n], btc)
                #print(buy_list[n],"익절 돔황차!!!!")
                #buy_list[n] = ""
                #buy_price[n] = 0
         else:
             i = 0
             if asd == 0:
              for n in range(0,2):
               btc = get_balance(buy_list[n])   
               if btc != 0:
                upbit.sell_market_order("KRW-"+buy_list[n], btc)
                print("KRW-"+ buy_list[n],"전량매도")
              print("다시 한번 뜨거운 승부를") 
              target_list = [0 for i in range(len(les))]
              buy_list = ["",""]
              buy_price = [0,0]
              bought_list = []
              asd = 1        
             while True:
              try: 
               start_time = get_start_time(coin)
               end_time = start_time + datetime.timedelta(days=1)- datetime.timedelta(minutes=2)
               break
              except Exception as e:
               continue
         i = i + 1 
     else:
      i = 0             
    except Exception as e:
     print(e)
     i = i + 1
