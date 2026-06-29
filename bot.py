import yfinance as yf
import telebot
import os

# 깃허브 설정(Secrets)에서 가져올 값들
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
bot = telebot.TeleBot(TOKEN)

portfolio = [
    {"name": "나스닥100", "symbol": "QQQ", "buy_price": 400.0, "quantity": 10},
    {"name": "삼성전자", "symbol": "005930.KS", "buy_price": 70000, "quantity": 50}
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
