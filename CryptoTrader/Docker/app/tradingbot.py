import json
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime, timedelta
from alpaca_trade_api import REST
from Docker.app.finbert_utils import estimate_sentiment

BASE_URL = "https://paper-api.alpaca.markets/v2"

class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.secrets = self.get_secrets()
        self.api = REST(base_url=BASE_URL, key_id=secrets.get('API_KEY'), secret_key=secrets.get('API_SECRET'))
                        
    def get_secrets():
        with open('secrets.json') as secrets_file:
            return json.load(secrets_file)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)

        return cash, last_price, quantity

    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today)
        news = [ev.__dict__['_raw']['headline'] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price:
            if sentiment == 'positive' and probability > 0.999:
                if self.last_trade == 'sell':
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    'buy',
                    take_profit_price=last_price*1.20,
                    stop_loss_price=last_price*0.95
                )
                self.submit_order(order)
                self.last_trade = 'buy'
            elif sentiment == 'negative' and probability > 0.999:
                if self.last_trade == 'buy':
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    'sell',
                    take_profit_price=last_price*0.8,
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order)
                self.last_trade = 'sell'

def get_secrets():
    with open('secrets.json') as secrets_file:
        return json.load(secrets_file)
    
secrets = get_secrets()
APACA_CREDS = {
    "API_KEY": secrets.get("API_KEY"),
    "API_SECRET": secrets.get("API_SECRET"),
    "PAPER": secrets.get("PAPER"),
}
    
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)
broker = Alpaca(APACA_CREDS)
strategy = MLTrader(name='mlstrat', 
                    broker=broker,
                    parameters={
                        'symbol': 'SPY',
                        'cash_at_risk': 0.5
                    })
#strategy.backtest(
#    YahooDataBacktesting,
#    start_date,
#    end_date,
#    parameters={
#        'symbol': 'SPY',
#        'cash_at_risk': 0.5
#    }
#)

trader = Trader()
trader.add_strategy(strategy)
trader.run_all()

 