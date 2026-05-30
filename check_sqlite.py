# check_sqlite.py
import os
import sqlite3

DB_PATH = "data/blockchain.db"

def check():
    print("=" * 50)
    print("ДИАГНОСТИКА SQLITE")
    print("=" * 50)
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    # Проверяем lock файлы
    wal_file = DB_PATH + "-wal"
    shm_file = DB_PATH + "-shm"
    
    if os.path.exists(wal_file):
        print(f"⚠️ Найден WAL файл: {wal_file}")
        print("   Возможно, есть незавершённые транзакции")
    
    if os.path.exists(shm_file):
        print(f"⚠️ Найден SHM файл: {shm_file}")
    
    # Пытаемся открыть БД
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("✅ База данных доступна")
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Таблицы: {tables}")
        
        # Проверяем балансы
        if 'wallets' in tables:
            cursor.execute("SELECT COUNT(*) FROM wallets")
            count = cursor.fetchone()[0]
            print(f"💰 Кошельков: {count}")
            
            cursor.execute("SELECT balance FROM wallets LIMIT 1")
            sample = cursor.fetchone()
            if sample:
                print(f"📈 Пример баланса: {sample[0]} (тип: {type(sample[0]).__name__})")
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"❌ Ошибка доступа: {e}")
        print("   Возможно, БД заблокирована другим процессом")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check()
