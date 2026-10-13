import yfinance as yf
from datetime import datetime

def fetch_crypto_data():
    print("Запрос актуальных котировок с серверов Yahoo Finance...")
    
    # Задаем тикеры криптовалют в формате Yahoo: BTC-USD, ETH-USD
    targets = ["BTC-USD", "ETH-USD"]
    
    try:
        cleaned_data = []
        dt_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for ticker_name in targets:
            # Инициализируем тикер yfinance
            ticker = yf.Ticker(ticker_name)
            
            # fast_info содержит актуальную живую цену в реальном времени
            price = round(ticker.fast_info['lastPrice'], 2)
            
            # Приводим имя к красивому стандарту для нашей базы данных (BTC_USD)
            symbol = ticker_name.replace("-", "_")
            
            print(f"[{dt_now}] {symbol} | Живой рыночный курс: ${price:,.2f}")
            
            cleaned_data.append({
                "symbol": symbol,
                "price": price,
                "timestamp": dt_now
            })
            
        print("\n УСПЕХ! Живые данные из интернета успешно обработаны.")
        return cleaned_data

    except Exception as e:
        print(f"\n[ОШИБКА НА ЭТАПЕ EXTRACT]: Не удалось прочитать данные Yahoo.")
        print(f"Детали ошибки: {e}")
        return None

if __name__ == "__main__":
    fetch_crypto_data()
