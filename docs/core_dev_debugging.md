# docs/core_dev_debugging.md
# Как реально чинят Ethereum-клиенты в mainnet

## Когда что-то ломается в Geth:
❌ никто не "смотрит логи и чинит баг"
🟢 они воспроизводят состояние сети как машину времени

## Шаг 1 — FREEZE STATE (КРИТИЧЕСКИЙ ШАГ)
- Останавливают node
- Сохраняют DB snapshot
- Фиксируют block height
- Цель: 🔒 "заморозить момент расхождения"

## Шаг 2 — TRACE BLOCK EXECUTION
- Берут конкретный block hash
- tx list
- state root before/after
- Re-execute block локально
- Вопрос: "почему execution diverged?"

## Шаг 3 — REPLAY ENGINE
Инструменты:
- debug replay mode
- deterministic re-execution
- state diff checker

Процесс: block → EVM re-run → compare state root

## Шаг 4 — STATE DIFF ANALYSIS
Core dev смотрит:
- which account changed
- which storage slot diverged
- which opcode caused divergence

Пример: slot 0x3f2 changed unexpectedly

## Шаг 5 — ROOT CAUSE CLASSIFICATION
Каждый bug относится к классу:
- 🟢 Execution bug (EVM opcode issue)
- 🟡 Consensus bug (fork-choice inconsistency)
- 🔴 Networking bug (bad peer data)
- 🔵 DB bug (corrupted state)

## Шаг 6 — CROSS-CLIENT VERIFICATION
Проверяют:
- Geth
- Nethermind
- Erigon

Если только 1 клиент ломается → local bug
Если все ломаются → protocol bug

## Шаг 7 — FUZZING & REPRODUCTION
- randomized tx generation
- adversarial block crafting
- state fuzzing
Цель: воспроизвести bug 100%

## Шаг 8 — PATCH + TEST SUITE ADDITION
Правило Ethereum:
"Every bug becomes a test forever"

## Шаг 9 — MAINNET ROLLOUT SAFETY
Patch НЕ сразу в mainnet:
- devnet
- testnet
- shadow fork testing

## Главный инструмент core dev
Они НЕ используют: ❌ print logs

Они используют:
🟢 execution tracer
🟢 state diff engine
🟢 fork replay system
🟢 consensus simulator

## Ментальная модель debugging
INPUT (block + tx) → EXECUTION → STATE OUTPUT → COMPARE ACROSS CLIENTS

## Самый опасный тип бага
"silent divergence bug"
- нет crash
- нет error
- но state differs by 1 slot

Это 🔴 худший возможный Ethereum bug
