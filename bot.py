import yfinance as yf
import telebot
import os

# 깃허브 설정(Secrets)에서 가져올 값들
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
bot = telebot.TeleBot(TOKEN)

portfolio = [
    {"name": "PLUS 선진국MSCI(합성H)", "symbol": "195970.KS", "buy_price": 15935, "quantity": 63},
    {"name": "kodex 200", "symbol": "069500.KS", "buy_price": 134140, "quantity": 7},
    {"name": "KODEX 미국S&P500", "symbol": "379800.KS", "buy_price": 25352, "quantity": 49}
]

def send_report():
    report = "📈 오늘의 투자 수익률 보고\n\n"
    for item in portfolio:
        stock = yf.Ticker(item['symbol'])
        # 최신 종가 가져오기
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        profit_rate = ((current_price - item['buy_price']) / item['buy_price']) * 100
        
        report += f"[{item['name']}]\n"
        report += f"수익률: {profit_rate:.2f}%\n"
        report += f"현재가: {current_price:,.0f}\n\n"
    
    bot.send_message(CHAT_ID, report)

if __name__ == "__main__":
    send_report()
