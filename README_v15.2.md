# Absolute Blockchain Ultimate v15.2

## 🎉 Integer Economics!

**Breaking Change**: Все балансы теперь хранятся в сатоши (int)!

- 1 ABS = 1,000,000 сатоши
- Больше никаких float проблем
- Детерминированная арифметика

## 🔐 Security Improvements

- Реальная проверка подписи (HMAC-SHA256)
- Challenge-response аутентификация
- JWT токены с refresh

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Blockchain stats |
| GET | `/api/auth/verify` | Verify JWT token |
| GET | `/api/auth/stats` | Auth subsystem stats |
| POST | `/api/auth/challenge` | Get challenge |
| POST | `/api/auth/login` | Login with signature |
| POST | `/api/auth/refresh` | Refresh token |
| POST | `/api/auth/logout` | Logout |

## 🚀 Migration

```bash
# Stop blockchain, then:
python migrate_to_int.py
``"

## 📄 License

MIT
