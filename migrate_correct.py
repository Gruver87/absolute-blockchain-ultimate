# migrate_correct.py
import sqlite3
import os
import time

DB_PATH = "data/blockchain.db"
# Правильный масштаб - как Bitcoin: 1 ABS = 100_000_000 сатоши
SATOSHI_MULTIPLIER = 100_000_000
MAX_INT64 = 9_223_372_036_854_775_807

def migrate():
    print("=" * 60)
    print("ПРАВИЛЬНАЯ МИГРАЦИЯ НА INTEGER ECONOMICS")
    print("=" * 60)
    print(f"1 ABS = {SATOSHI_MULTIPLIER} сатоши")
    print(f"MAX INT64: {MAX_INT64}")
    print()
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        
        # Начинаем транзакцию
        cursor.execute("BEGIN TRANSACTION")
        
        # Проверяем существующие таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Найдены таблицы: {tables}")
        
        # Миграция wallets
        if 'wallets' in tables:
            cursor.execute("PRAGMA table_info(wallets)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'balance' in columns:
                cursor.execute("SELECT rowid, address, balance FROM wallets")
                wallets = cursor.fetchall()
                print(f"\n💰 Найдено кошельков: {len(wallets)}")
                
                count = 0
                for rowid, address, balance in wallets:
                    if isinstance(balance, float):
                        # Конвертируем с правильным масштабом
                        new_balance = int(balance * SATOSHI_MULTIPLIER)
                        
                        # Проверка на переполнение
                        if new_balance > MAX_INT64:
                            print(f"   ⚠️ Баланс {address} слишком большой, обрезаем")
                            new_balance = MAX_INT64
                        
                        cursor.execute("UPDATE wallets SET balance = ? WHERE rowid = ?", (new_balance, rowid))
                        count += 1
                        
                        if count <= 5:
                            print(f"   ✅ {address}: {balance} -> {new_balance} сатоши")
                
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
        
        # Переносим балансы из wallets
        if 'wallets' in tables:
            cursor.execute("SELECT address, balance FROM wallets")
            print("\n📦 Перенос балансов в balances_satoshi...")
            
            for address, balance in cursor.fetchall():
                if isinstance(balance, int):
                    balance_satoshi = balance
                else:
                    balance_satoshi = int(balance * SATOSHI_MULTIPLIER)
                
                if balance_satoshi > MAX_INT64:
                    balance_satoshi = MAX_INT64
                
                cursor.execute('''
                    INSERT OR REPLACE INTO balances_satoshi (address, balance_satoshi, updated_at)
                    VALUES (?, ?, ?)
                ''', (address, balance_satoshi, int(time.time())))
            
            conn.commit()
            print("   ✅ Балансы перенесены")
        
        # Проверяем целостность
        cursor.execute("SELECT COUNT(*) FROM balances_satoshi")
        count = cursor.fetchone()[0]
        print(f"\n📊 Итог: {count} записей в balances_satoshi")
        
        # Завершаем транзакцию
        conn.commit()
        print("\n✅ Миграция завершена УСПЕШНО!")
        
    except sqlite3.OperationalError as e:
        print(f"\n❌ Ошибка SQLite: {e}")
        if conn:
            conn.rollback()
        print("   Возможно, база данных заблокирована")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.execute("PRAGMA wal_checkpoint")
            conn.close()
            print("🔒 Соединение закрыто")
    
    print("=" * 60)

if __name__ == "__main__":
    migrate()
