# migrate_to_int.py
import sqlite3
import os
import time

DB_PATH = "data/blockchain.db"
SATOSHI_MULTIPLIER = 1_000_000

def migrate():
    print("=" * 50)
    print("МИГРАЦИЯ НА INTEGER ECONOMICS")
    print("=" * 50)
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    if 'wallets' in tables:
        cursor.execute("PRAGMA table_info(wallets)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'balance' in columns:
            cursor.execute("SELECT rowid, balance FROM wallets")
            wallets = cursor.fetchall()
            count = 0
            for rowid, balance in wallets:
                if isinstance(balance, float):
                    new_balance = int(balance * SATOSHI_MULTIPLIER)
                    cursor.execute("UPDATE wallets SET balance = ? WHERE rowid = ?", (new_balance, rowid))
                    count += 1
            print(f"✅ Конвертировано кошельков: {count}")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balances_satoshi (
            address TEXT PRIMARY KEY,
            balance_satoshi INTEGER DEFAULT 0,
            updated_at INTEGER
        )
    ''')
    
    if 'wallets' in tables:
        cursor.execute("SELECT address, balance FROM wallets")
        for address, balance in cursor.fetchall():
            if isinstance(balance, int):
                balance_satoshi = balance
            else:
                balance_satoshi = int(balance * SATOSHI_MULTIPLIER)
            cursor.execute('''
                INSERT OR REPLACE INTO balances_satoshi (address, balance_satoshi, updated_at)
                VALUES (?, ?, ?)
            ''', (address, balance_satoshi, int(time.time())))
    
    conn.commit()
    conn.close()
    
    print("✅ Миграция завершена!")
    print("⚠️ 1 ABS = 1_000_000 сатоши")
    print("=" * 50)

if __name__ == "__main__":
    migrate()
