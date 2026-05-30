# diagnose_db.py
import sqlite3
import os

DB_PATH = "data/blockchain.db"

def diagnose():
    print("=" * 60)
    print("ДИАГНОСТИКА БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    # Проверяем lock файлы
    for ext in ['', '-wal', '-shm', '-journal']:
        f = DB_PATH + ext
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"📁 {os.path.basename(f)}: {size} bytes")
    
    print()
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Таблицы: {tables}")
        
        # Проверяем balances_satoshi
        if 'balances_satoshi' in tables:
            cursor.execute("SELECT COUNT(*) FROM balances_satoshi")
            count = cursor.fetchone()[0]
            print(f"💰 Записей в balances_satoshi: {count}")
            
            cursor.execute("SELECT address, balance_satoshi FROM balances_satoshi LIMIT 3")
            for addr, bal in cursor.fetchall():
                print(f"   {addr}: {bal} сатоши")
        
        # Проверяем wallets
        if 'wallets' in tables:
            cursor.execute("SELECT COUNT(*) FROM wallets")
            count = cursor.fetchone()[0]
            print(f"💰 Записей в wallets: {count}")
            
            cursor.execute("SELECT address, balance FROM wallets LIMIT 3")
            for addr, bal in cursor.fetchall():
                print(f"   {addr}: {bal}")
        
        conn.close()
        print("\n✅ Диагностика завершена")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    diagnose()
