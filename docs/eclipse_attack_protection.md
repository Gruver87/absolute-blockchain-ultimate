# docs/eclipse_attack_protection.md
# P2P Eclipse Attack — как изолируют ноду

## Атака
Злоумышленник окружает ноду фейковыми peer'ами

## Эффект
Node sees ONLY attacker network

## Последствия
- Fake chain accepted
- Real chain hidden
- Transaction censorship

## Защита
- Peer diversity enforcement
- Trusted seeds
- Random peer rotation
- Outbound connection limits
