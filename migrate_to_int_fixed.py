# migrate_to_int_fixed.py
import sqlite3
import os
import time

DB_PATH = "data/blockchain.db"
# Правильный масштаб - 1 ABS = 100_000_000 сатоши (как Bitcoin)
SATOSHI_MULTIPLIER = 100_000_000

def migrate():
    print("=" * 50)
    print("МИГРАЦИЯ НА INTEGER ECONOMICS (FIXED)")
    print("=" * 50)
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    # Закрываем все соединения
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Проверяем существующие таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'wallets' in tables:
            cursor.execute("PRAGMA table_info(wallets)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'balance' in columns:
                # Получаем все кошельки
                cursor.execute("SELECT rowid, address, balance FROM wallets")
                wallets = cursor.fetchall()
                count = 0
                
                for rowid, address, balance in wallets:
                    # Конвертируем float в int с правильным масштабом
                    if isinstance(balance, float):
                        # Проверяем на переполнение
                        new_balance = int(balance * SATOSHI_MULTIPLIER)
                        if new_balance > 9_223_372_036_854_775_807:
                            print(f"⚠️ Баланс {address} слишком большой, обрезаем до MAX_INT64")
                            new_balance = 9_223_372_036_854_775_807
                        cursor.execute("UPDATE wallets SET balance = ? WHERE rowid = ?", (new_balance, rowid))
                        count += 1
                        print(f"   Конвертирован {address}: {balance} -> {new_balance} сатоши")
                
                conn.commit()
                print(f"\n✅ Конвертировано кошельков: {count}")
        
        # Создаём новую таблицу для сатоши
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balances_satoshi (
                address TEXT PRIMARY KEY,
                balance_satoshi INTEGER DEFAULT 0,
                updated_at INTEGER
            )
        ''')
        
        # Переносим балансы
        if 'wallets' in tables:
            cursor.execute("SELECT address, balance FROM wallets")
            for address, balance in cursor.fetchall():
                if isinstance(balance, int):
                    balance_satoshi = balance
                else:
                    balance_satoshi = int(balance * SATOSHI_MULTIPLIER)
                
                # Проверка на переполнение
                if balance_satoshi > 9_223_372_036_854_775_807:
                    balance_satoshi = 9_223_372_036_854_775_807
                
                cursor.execute('''
                    INSERT OR REPLACE INTO balances_satoshi (address, balance_satoshi, updated_at)
                    VALUES (?, ?, ?)
                ''', (address, balance_satoshi, int(time.time())))
        
        conn.commit()
        
        # Проверяем WAL файлы
        cursor.execute("PRAGMA wal_checkpoint;")
        
        conn.close()
        
        print("\n✅ Миграция завершена успешно!")
        print(f"⚠️ 1 ABS = {SATOSHI_MULTIPLIER} сатоши")
        print("=" * 50)
        
    except sqlite3.OperationalError as e:
        print(f"❌ Ошибка БД: {e}")
        print("   Возможно, блокчейн запущен. Остановите его и попробуйте снова.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    migrate()
