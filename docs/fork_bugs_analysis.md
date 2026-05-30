# docs/fork_bugs_analysis.md
# Fork Bugs — самый опасный класс ошибок в Ethereum клиентах

## Проблема
Две ноды считают разные цепи "истинными"

## Реальный сценарий
- Node A: chain A wins
- Node B: chain B wins

## Причины
- Race condition в fork-choice
- Delayed attestations
- Inconsistent state root validation

## Эффект
Сеть временно "раздваивается"

## Защита
- LMD-GHOST weight calculation
- Reorg limit (MAX_REORG_DEPTH)
- Cross-client verification
