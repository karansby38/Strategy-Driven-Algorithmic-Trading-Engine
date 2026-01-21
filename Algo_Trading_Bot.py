#!/usr/bin/env python
# coding: utf-8

# In[72]:


from datetime import datetime
import yfinance as yf
import time


# In[73]:


class TradingStrategy:
    def __init__(self,name):
        self.__name=name
    def generate_signal(self,price_data):
        print("The method is to be overriden")
        return "Hold"

    @property
    def name(self):
        return self.__name


# In[74]:


class SmaTradeStrategy(TradingStrategy):
    def __init__(self,swin,lwin):
        super().__init__("SMA Trading Strategy")
        self.__swin=swin
        self.__lwin=lwin

    def generate_signal(self,price_data):
        if len(price_data[-self.__lwin:])<self.__lwin:
            return "Hold"
        long_avg=sum(price_data[-self.__lwin:])/self.__lwin
        short_avg= sum(price_data[-self.__swin:])/self.__swin

        if short_avg>long_avg:
                       return "Buy"
        elif short_avg<long_avg:
                       return "Sell"
        else:
                       return "Hold"

    @property
    def swin(self):
        return self.__swin
    @property
    def lwin(self):
        return self.__lwin






# In[75]:


class Mytrade:
    def __init__(self,strat_name,signal,amount):
        self.__strat_name=strat_name
        self.__signal=signal
        self.__amount=amount
        self.__time=datetime.now()

    def execute(self): 
        print(f"Executed {self.__signal} trade with {self.__strat_name} at amount {self.__amount} on {self.__time} ")

    @property
    def strat_name(self):
        return self.__strat_name
    @property
    def signal(self):
        return self.__signal
    @property
    def amount(self):
        return self.__amount
    @property
    def time(self):
        return self.__time


# In[76]:


class TradingAPI:
    def __init__(self, balance):
        self.__balance = balance
        self.__position = 0

    def place_order(self, trade, price):
        if trade.signal == "Buy" and self.__balance >= price:
            self.__balance -= price
            self.__position += 1
            print(f"BUY @ {price} | Balance: {self.__balance}")

        elif trade.signal == "Sell" and self.__position > 0:
            self.__balance += price
            self.__position -= 1
            print(f"SELL @ {price} | Balance: {self.__balance}")

    @property
    def balance(self):
        return self.__balance



# In[77]:


class TradeEngine:
    def __init__(self,symbol,api,strategy):
        self.__sym=symbol
        self.__api=api
        self.__strategy=strategy
        self.__price_data=[]

    def fetch_price_data(self):
        data = yf.download(self.__sym, period="5d", interval="1m")

        closes = data['Close'].iloc[:, 0].dropna().astype(float).tolist()

        # feed candles one by one
        if len(self.__price_data) < len(closes):
            price = closes[len(self.__price_data)]
            self.__price_data.append(price)
            print(f"Fetched historical price: {price}")



    def run(self):                            #integrates all the classes
        self.fetch_price_data()
        signal=self.__strategy.generate_signal(self.__price_data)
        print(f"Generated Signal: {signal}")
        if signal in ["Buy","Sell"]:
            trade= Mytrade(self.__strategy.name,signal,1)
            trade.execute()
            self.__api.place_order(trade,self.__price_data[-1])

    @property
    def strategy(self):
        return self.__strategy
    @property
    def sym(self):
        return self.__sym
    @property
    def api(self):
        return self.__api
    @property
    def balance(self):
        return self.__price_data



# In[79]:


sym='AAPL'
api= TradingAPI(balance=10000)
strategy=SmaTradeStrategy(1,3)
system= TradeEngine(sym,api,strategy)

for _ in range(10):
    system.run()
    time.sleep(60)


# In[ ]:





# In[ ]:




