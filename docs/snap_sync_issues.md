# docs/snap_sync_issues.md
# Snap Sync Edge Cases — как ломается fast sync

## Проблема
Snap sync получает:
- Incomplete snapshot
- Inconsistent trie nodes

## Сценарий
Node trusts snapshot → but snapshot is invalid

## Результат
Corrupted local state
Forced resync

## Защита
- Snapshot verification
- Chunk validation
- Fallback to full sync
- Multiple peer verification
