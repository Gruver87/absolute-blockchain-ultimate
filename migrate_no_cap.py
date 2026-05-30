# migrate_no_cap.py
import sqlite3
import os
import time

DB_PATH = "data/blockchain.db"
SATOSHI_MULTIPLIER = 100_000_000
# Убираем обрезание - просто проверяем, но не обрезаем

def migrate():
    print("=" * 60)
    print("МИГРАЦИЯ (БЕЗ ОБРЕЗАНИЯ)")
    print("=" * 60)
    print(f"1 ABS = {SATOSHI_MULTIPLIER} сатоши")
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    if 'balances_satoshi' in tables:
        cursor.execute("SELECT address, balance_satoshi FROM balances_satoshi")
        balances = cursor.fetchall()
        print(f"\n💰 Найдено записей: {len(balances)}")
        
        total = 0
        for address, balance in balances:
            total += balance
            print(f"   {address}: {balance}")
        
        print(f"\n💰 Total supply: {total} сатоши ({total / SATOSHI_MULTIPLIER:.6f} ABS)")
    else:
        print("❌ Таблица balances_satoshi не найдена")
    
    conn.close()
    print("=" * 60)

if __name__ == "__main__":
    migrate()
