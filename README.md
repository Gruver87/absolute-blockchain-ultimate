# ⚡ Absolute Blockchain Ultimate

> **Experimental L1 Blockchain Framework | UTXO | P2P | DPoS | NFT | Sharding | Post-Quantum**

| Status | Version | Goal |
|--------|---------|------|
| 🧪 Experimental / Alpha | v15.2 | Production-ready Blockchain |

---

## 🚨 DISCLAIMER

**THIS IS EXPERIMENTAL SOFTWARE**

| ❌ | Description |
|---|---|
| **NOT production-ready** | For testing only |
| Data may be reset | No balance guarantees |
| Bugs expected | Unstable operation |
| Security not guaranteed | No audit yet |
| API may change | Without notice |

---

## 📖 About

Absolute Blockchain is an **experimental blockchain framework** built from scratch.

### ✅ Implemented

| Component | Description |
|-----------|-------------|
| 🔗 Core | UTXO, DPoS, Merkle Patricia Tree |
| 🌐 P2P | Peer discovery & sync |
| 💰 Economics | 1 ABS = 100M satoshi (no float) |
| 🦋 NFT | Minting, collections, royalties |
| 💱 DEX | Liquidity pools, swaps |
| ⚡ Lightning | Off-chain payments |
| 🌉 Bridges | ETH, BSC, SOL, POL |
| 🔐 Quantum | SPHINCS+ |
| 📊 Sharding | 64 shards |
| 🔌 EVM/WASM | Smart contracts |
| 🧠 AI | PoUW agents |
| 🔒 JWT Auth | Access/Refresh tokens |
| 🛡️ Rate Limit | 60 req/min |

### 🚧 In Progress

- Full validation
- Canonical serialization
- Replay protection
- Testnet (v16.0)
- Security audit
- Mainnet launch

---

## 🎯 Network Goals

| Metric | Target |
|--------|--------|
| Consensus | DPoS + PoUW |
| TPS | 10,000+ |
| Block time | 10 sec |
| Max supply | 210,000,000 ABS |
| Quantum safe | SPHINCS+ |
| Smart contracts | EVM + WASM |

---

## 🌐 Ports & Services

| Service | Port | URL |
|---------|------|-----|
| Main API | 8080 | http://localhost:8080 |
| API Docs | 8080 | http://localhost:8080/docs |
| Testnet | 8088 | http://localhost:8088 |
| Explorer | 8090 | http://localhost:8090 |
| GUI | 8091 | http://localhost:8091 |
| Monitor | 8092 | http://localhost:8092 |
| Mobile API | 8093 | http://localhost:8093 |
| Web Server | 8094 | http://localhost:8094 |
| Auto Heal | 8095 | http://localhost:8095 |
| P2P | 5000-5002 | - |
| Metrics | 9090 | http://localhost:9090/metrics |

---

## 📡 API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| Health | `GET /api/health` | Health check |
| Stats | `GET /api/stats` | Blockchain stats |
| Mempool | `GET /api/mempool/stats` | Pending txs |
| Wallet | `POST /api/wallet/create` | New wallet |
| Balance | `GET /api/balance?address=` | Check balance |
| Send | `POST /api/transaction/send` | Send transaction |
| Mine | `POST /api/mine` | Mine block |
| Auth | `POST /api/auth/challenge` | Get challenge |
| Auth | `POST /api/auth/login` | Login with signature |
| Auth | `GET /api/auth/verify` | Verify JWT |
| Auth | `GET /api/auth/stats` | Auth stats |
| NFT | `POST /api/nft/collection/create` | Create collection |
| NFT | `POST /api/nft/mint` | Mint NFT |
| NFT | `GET /api/nft/tokens` | List NFTs |
| NFT | `GET /api/nft/stats` | NFT stats |

---

## 📡 API Examples

### Health & Stats
```bash
curl http://localhost:8080/api/health
curl http://localhost:8080/api/stats
curl http://localhost:8080/api/mempool/stats
Wallet & Balance
bash
curl -X POST http://localhost:8080/api/wallet/create
curl http://localhost:8080/api/balance?address=foundation
Transaction & Mining
bash
curl -X POST http://localhost:8080/api/transaction/send \
  -H "Content-Type: application/json" \
  -d '{"from":"foundation","to":"test","amount":100,"private_key":"test"}'

curl -X POST http://localhost:8080/api/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"foundation"}'
Authentication
bash
curl -X POST http://localhost:8080/api/auth/challenge \
  -H "Content-Type: application/json" \
  -d '{"address":"foundation"}'

curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"address":"foundation","nonce":"...","signature":"..."}'

curl http://localhost:8080/api/auth/verify \
  -H "Authorization: Bearer <token>"

curl http://localhost:8080/api/auth/stats
NFT
bash
curl -X POST http://localhost:8080/api/nft/collection/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Heroes","creator":"foundation","royalty":5}'

curl -X POST http://localhost:8080/api/nft/mint \
  -H "Content-Type: application/json" \
  -d '{"collection_id":"...","name":"Hero #1","creator":"foundation","owner":"foundation"}'

curl http://localhost:8080/api/nft/tokens
curl http://localhost:8080/api/nft/stats
🚀 Quick Start
bash
# Clone
git clone https://github.com/Gruver87/absolute-blockchain-ultimate.git
cd absolute-blockchain-ultimate

# Install
pip install -r requirements.txt

# Run
python ABSOLUTE_FINAL_FIXED.py
Multi-window Launch
WindowCommand
1python ABSOLUTE_FINAL_FIXED.py
2python telegram_super_bot.py
3python testnet.py
4python explorer.py
5python gui.py
6python monitor.py
Stop All
powershell
Get-Process python | Stop-Process -Force
🐳 Docker
bash
# Build
docker build -t absolute-blockchain .

# Run (all ports)
docker run -d -p 8080:8080 -p 8088:8088 -p 8090:8095 -p 9090:9090 -p 5000:5000 absolute-blockchain

# Run (minimal)
docker run -p 8080:8080 absolute-blockchain
📊 Monitoring
Prometheus metrics: http://localhost:9090/metrics

MetricDescription
blockchain_blocks_totalTotal blocks
blockchain_transactions_totalTotal transactions
blockchain_peers_countPeer count
blockchain_pending_txMempool size
auth_active_sessionsActive sessions
🧪 Test Data
Test Wallets
AddressBalancePrivate Key (test)
foundation~100M ABStest
test~50K ABStest
genesis~10K ABSgenesis
Faucet
text
http://localhost:8088/api/testnet/faucet/claim
📚 Documentation
API Docs: http://localhost:8080/docs

Whitepaper: http://localhost:8094/whitepaper.html

Landing Page: http://localhost:8094/landing_page.html

📄 License
MIT License © 2025 Absolute Blockchain

🔗 Links
GitHub Repository

Releases

Issues

⚠️ REMINDER: Experimental project — NOT for production use!
