# fix_total_supply_correct.py
import sqlite3
import os

DB_PATH = "data/blockchain.db"
SATOSHI_MULTIPLIER = 100_000_000

def fix_supply():
    print("=" * 60)
    print("ФИКСАЦИЯ TOTAL_SUPPLY (ПРАВИЛЬНАЯ)")
    print("=" * 60)
    
    if not os.path.exists(DB_PATH):
        print("❌ База данных не найдена")
        return
    
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    
    try:
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'balances_satoshi' in tables:
            # Получаем все балансы по одному (избегаем integer overflow)
            cursor.execute("SELECT address, balance_satoshi FROM balances_satoshi")
            balances = cursor.fetchall()
            
            total_satoshi = 0
            print("\n📊 Балансы:")
            for address, balance in balances:
                total_satoshi += balance
                print(f"   {address}: {balance} сатоши")
            
            total_abs = total_satoshi / SATOSHI_MULTIPLIER
            print(f"\n💰 Total supply (сатоши): {total_satoshi}")
            print(f"💰 Total supply (ABS): {total_abs:.6f}")
            
            # Сохраняем статистику
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS supply_stats (
                    id INTEGER PRIMARY KEY,
                    total_supply_satoshi INTEGER,
                    total_supply_abs REAL,
                    calculated_at INTEGER
                )
            ''')
            
            cursor.execute('''
                INSERT INTO supply_stats (total_supply_satoshi, total_supply_abs, calculated_at)
                VALUES (?, ?, ?)
            ''', (total_satoshi, total_abs, int(__import__('time').time())))
            
            conn.commit()
            print("\n✅ Total supply зафиксирован")
        else:
            print("❌ Таблица balances_satoshi не найдена")
            
    except sqlite3.OperationalError as e:
        print(f"❌ Ошибка SQLite: {e}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()
    
    print("=" * 60)

if __name__ == "__main__":
    fix_supply()
