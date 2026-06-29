import yfinance as yf
import telebot
import os

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = "8632143584" # 본인의 Chat ID 숫자를 넣으세요
bot = telebot.TeleBot(TOKEN)

# 종목 설정
portfolio = [
    {"name": "PLUS 선진국MSCI(합성H)", "symbol": "195970.KS", "buy_price": 15935, "quantity": 63},
    {"name": "kodex 200", "symbol": "069500.KS", "buy_price": 134140, "quantity": 7},
    {"name": "KODEX 미국S&P500", "symbol": "379800.KS", "buy_price": 25352, "quantity": 49}# 추가 종목이 있다면 여기에 계속 넣으세요
]

def send_report():
    report = "💰 오늘의 투자 수익 보고\n\n"
    total_buy_sum = 0
    total_current_sum = 0

    for item in portfolio:
        try:
            stock = yf.Ticker(item['symbol'])
            hist = stock.history(period="5d")
            if hist.empty:
                report += f"⚠️ {item['name']}: 데이터를 찾을 수 없음\n\n"
                continue
                
            current_price = hist['Close'].iloc[-1]
            buy_total = item['buy_price'] * item['quantity']
            current_total = current_price * item['quantity']
            
            profit_loss = current_total - buy_total # 수익금
            profit_rate = (profit_loss / buy_total) * 100 # 수익률
            
            report += f"🔹 [{item['name']}]\n"
            report += f"평가금액: {current_total:,.0f}원\n"
            report += f"수익금: {profit_loss:+,,.0f}원 ({profit_rate:+.2f}%)\n"
            report += f"현재가: {current_price:,.0f}원\n\n"
            
            total_buy_sum += buy_total
            total_current_sum += current_total
            
        except Exception as e:
            report += f"❌ {item['name']} 에러: {str(e)}\n\n"

    if total_buy_sum > 0:
        total_profit_loss = total_current_sum - total_buy_sum
        total_profit_rate = (total_profit_loss / total_buy_sum) * 100
        
        report += f"--------------------\n"
        report += f"📊 [총 합계]\n"
        report += f"총 매수금액: {total_buy_sum:,.0f}원\n"
        report += f"총 평가금액: {total_current_sum:,.0f}원\n"
        report += f"총 수익금액: {total_profit_loss:+,,.0f}원\n"
        report += f"총 수익률: {total_profit_rate:+.2f}%"
    
    bot.send_message(CHAT_ID, report)

if __name__ == "__main__":
    send_report()
