# docs/state_corruption_handling.md
# State Trie Corruption — катастрофа для Ethereum

## Проблема
Merkle Patricia Trie ломается из-за:
- Disk write failure
- Partial update
- Crash during commit

## Результат
Same block → different state root

## Это КАТАСТРОФА потому что:
state root = truth of Ethereum

## Решения
- Write-ahead log (WAL)
- Periodic snapshots
- Crash recovery
- State root verification
