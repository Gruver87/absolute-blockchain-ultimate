# fix_total_supply.py
import sqlite3
import os

DB_PATH = "data/blockchain.db"
SATOSHI_MULTIPLIER = 100_000_000

def fix_supply():
    print("=" * 60)
    print("ФИКСАЦИЯ TOTAL_SUPPLY")
    print("=" * 60)
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    
    # Суммируем балансы
    cursor.execute("SELECT SUM(balance_satoshi) FROM balances_satoshi")
    result = cursor.fetchone()[0]
    
    if result:
        total_satoshi = int(result)
        total_abs = total_satoshi / SATOSHI_MULTIPLIER
        print(f"💰 Total supply (сатоши): {total_satoshi}")
        print(f"💰 Total supply (ABS): {total_abs}")
        
        # Сохраняем в отдельную таблицу
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS supply_stats (
                id INTEGER PRIMARY KEY,
                total_supply_satoshi INTEGER,
                total_supply_abs REAL,
                updated_at INTEGER
            )
        ''')
        
        cursor.execute('''
            INSERT INTO supply_stats (total_supply_satoshi, total_supply_abs, updated_at)
            VALUES (?, ?, ?)
        ''', (total_satoshi, total_abs, int(__import__('time').time())))
        
        conn.commit()
        print("\n✅ Total supply зафиксирован")
    else:
        print("❌ Нет данных в balances_satoshi")
    
    conn.close()
    print("=" * 60)

if __name__ == "__main__":
    fix_supply()
