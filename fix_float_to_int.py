# fix_float_to_int.py
# Скрипт для конвертации float балансов в int

import sqlite3
import os

DB_PATH = "data/blockchain.db"

def convert_balances():
    """Конвертирует все float балансы в int (сатоши)"""
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Проверяем наличие таблицы wallets
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='wallets'")
    if cursor.fetchone():
        # Конвертируем балансы
        cursor.execute("SELECT address, balance FROM wallets")
        wallets = cursor.fetchall()
        
        for address, balance in wallets:
            if isinstance(balance, float):
                new_balance = int(balance * 1_000_000)
                cursor.execute("UPDATE wallets SET balance = ? WHERE address = ?", (new_balance, address))
                print(f"✅ Конвертирован {address}: {balance} -> {new_balance} сатоши")
        
        conn.commit()
        print(f"\n✅ Конвертировано {len(wallets)} кошельков")
    
    conn.close()
    print("\n⚠️ ВНИМАНИЕ: Теперь балансы хранятся в сатоши (1 ABS = 1_000_000 сатоши)")

if __name__ == "__main__":
    convert_balances()
