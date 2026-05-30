-- Восстановление правильных балансов
UPDATE balances_satoshi SET balance_satoshi = 2999779999700000 WHERE address = 'foundation';
UPDATE balances_satoshi SET balance_satoshi = 2000000000000000 WHERE address = 'development';
UPDATE balances_satoshi SET balance_satoshi = 2000000000000000 WHERE address = 'community';
UPDATE balances_satoshi SET balance_satoshi = 2000000000000000 WHERE address = 'staking_rewards';
UPDATE balances_satoshi SET balance_satoshi = 1000000000000000 WHERE address = 'ecosystem';
UPDATE balances_satoshi SET balance_satoshi = 500000000000000 WHERE address = 'reserve';
UPDATE balances_satoshi SET balance_satoshi = 300000000000000 WHERE address = 'marketing';
UPDATE balances_satoshi SET balance_satoshi = 200000000000000 WHERE address = 'team';
UPDATE balances_satoshi SET balance_satoshi = 100000000000000 WHERE address = 'advisors';
UPDATE balances_satoshi SET balance_satoshi = 50000000000000 WHERE address = 'test';
UPDATE balances_satoshi SET balance_satoshi = 10000000000000 WHERE address = 'genesis';
