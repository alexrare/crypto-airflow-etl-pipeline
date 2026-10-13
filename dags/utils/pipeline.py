import sys
import os
# Жестко прописываем путь к текущей папке, чтобы Python внутри Docker не терял импорты
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sqlalchemy import create_engine, text
from extract import fetch_crypto_data  # Подтягиваем рабочий код из extract.py

def run_etl_pipeline():
    print("--- ЗАПУСК ETL ПАЙПЛАЙНА КРИПТОВАЛЮТЫ ---")
    
    # 1. ЭТАП EXTRACT (СБОР ДАННЫХ ИЗ ИНТЕРНЕТА)
    raw_data = fetch_crypto_data()
    if not raw_data:
        print("[ОШИБКА] Не удалось собрать данные из интернета.")
        return
        
    # 2. ЭТАП TRANSFORM (ОБРАБОТКА В PANDAS)
    # Превращаем данные в аналитическую таблицу DataFrame
    df = pd.DataFrame(raw_data)
    
    # 3. ЭТАП LOAD (ЗАГРУЗКА В SQL БАЗУ ДАННЫХ)
    # Указываем жесткий путь внутри контейнера Airflow, чтобы у Linux были права на запись
    engine = create_engine("sqlite:////opt/airflow/dags/crypto_project.db")
    
    print("\n[SQL] Запись данных в таблицу 'crypto_history'...")
    # if_exists='append' дописывает новые данные в конец таблицы, сохраняя историю
    df.to_sql("crypto_history", con=engine, if_exists="append", index=False)
    print(" Данные успешно сохранены!")
    
    # 4. ЭТАП АНАЛИТИКИ (ВЫПОЛНЕНИЕ SQL ЗАПРОСА)
    print("\n[SQL] Выполняем аналитический запрос к базе данных...")
    with engine.connect() as connection:
        # Пишем SQL-запрос с группировкой (GROUP BY) и агрегатными функциями (AVG, COUNT)
        query = text("""
            SELECT 
                symbol, 
                COUNT(*) as total_records, 
                ROUND(AVG(price), 2) as average_price,
                MAX(timestamp) as last_update
            FROM crypto_history 
            GROUP BY symbol;
        """)
        result = connection.execute(query)
        
        print("-----------------------------------------------------------------------------")
        print("SYMBOL   | ЗАПИСЕЙ В БД | СРЕДНЯЯ ЦЕНА     | ПОСЛЕДНЕЕ ОБНОВЛЕНИЕ")
        print("-----------------------------------------------------------------------------")
        
        for row in result:
            # Извлекаем значения из каждой колонки SQL-запроса по отдельности
            symbol = row.symbol
            total_records = row.total_records
            average_price = row.average_price
            last_update = row.last_update
            
            # Печатаем аккуратную ровную таблицу
            print(f"{symbol:<8} | {total_records:<12} | ${average_price:<15,} | {last_update}")
            
        print("-----------------------------------------------------------------------------")

if __name__ == "__main__":
    run_etl_pipeline()