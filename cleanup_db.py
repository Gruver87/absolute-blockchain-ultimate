# cleanup_db.py
import os
import time

DB_PATH = "data/blockchain.db"

def cleanup():
    print("=" * 50)
    print("ОЧИСТКА ФАЙЛОВ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    files = [DB_PATH, DB_PATH + "-wal", DB_PATH + "-shm", DB_PATH + "-journal"]
    
    for f in files:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"✅ Удалён: {f}")
            except Exception as e:
                print(f"⚠️ Не удалось удалить {f}: {e}")
    
    print("\n⚠️ Убедитесь, что блокчейн остановлен перед очисткой!")
    print("=" * 50)

if __name__ == "__main__":
    cleanup()
