# core/debug_tools.py
# Инструменты для production debugging

import hashlib
import json
import time
from typing import Dict, Any, List, Optional

class ExecutionTracer:
    """Trace execution for debugging"""
    
    def __init__(self):
        self.trace: List[Dict] = []
    
    def trace_execution(self, evm, tx, state) -> Dict:
        """Trace EVM execution step by step"""
        steps = []
        start_state = {
            "from_balance": state.get_balance(tx.get("from")),
            "to_balance": state.get_balance(tx.get("to")),
            "nonce": state.get_nonce(tx.get("from"))
        }
        
        result = evm.execute(tx, state)
        
        end_state = {
            "from_balance": state.get_balance(tx.get("from")),
            "to_balance": state.get_balance(tx.get("to")),
            "nonce": state.get_nonce(tx.get("from"))
        }
        
        self.trace.append({
            "tx": tx,
            "result": result,
            "start_state": start_state,
            "end_state": end_state,
            "gas_used": result.get("gas_used", 0)
        })
        
        return result
    
    def get_trace(self) -> List[Dict]:
        return self.trace
    
    def save_trace(self, path: str):
        with open(path, "w") as f:
            json.dump(self.trace, f, indent=2)

class StateDiffEngine:
    """Compare state differences between nodes"""
    
    def __init__(self):
        self.diffs: List[Dict] = []
    
    def compare_states(self, state_a: Dict, state_b: Dict) -> Dict:
        """Compare two states and return differences"""
        diffs = {}
        
        all_addresses = set(state_a.keys()) | set(state_b.keys())
        
        for addr in all_addresses:
            acc_a = state_a.get(addr, {"balance": 0, "nonce": 0})
            acc_b = state_b.get(addr, {"balance": 0, "nonce": 0})
            
            if acc_a != acc_b:
                diffs[addr] = {
                    "a": acc_a,
                    "b": acc_b,
                    "diff_balance": acc_b.get("balance", 0) - acc_a.get("balance", 0),
                    "diff_nonce": acc_b.get("nonce", 0) - acc_a.get("nonce", 0)
                }
        
        return diffs
    
    def format_diff(self, diff: Dict) -> str:
        """Format diff for human reading"""
        if not diff:
            return "✅ No differences"
        
        lines = ["📊 State differences found:"]
        for addr, data in diff.items():
            lines.append(f"   {addr}:")
            lines.append(f"      balance: {data['a'].get('balance')} → {data['b'].get('balance')}")
            lines.append(f"      nonce: {data['a'].get('nonce')} → {data['b'].get('nonce')}")
        return "\n".join(lines)

class ForkReplaySystem:
    """Replay chain forks for debugging"""
    
    def __init__(self, processor):
        self.processor = processor
        self.replay_log = []
    
    def replay_chain(self, blocks: List[Dict]) -> bool:
        """Replay chain from blocks"""
        for block_dict in blocks:
            # Convert dict to Block object if needed
            if hasattr(self.processor, 'process_block'):
                # Try to create Block object
                from geth_core.processor import Block
                if isinstance(block_dict, dict):
                    block = Block(
                        number=block_dict.get("number", 0),
                        transactions=block_dict.get("transactions", []),
                        parent_hash=block_dict.get("parent_hash", "0" * 64),
                        proposer=block_dict.get("proposer", "unknown")
                    )
                else:
                    block = block_dict
                
                success = self.processor.process_block(block)
                self.replay_log.append({
                    "block": block_dict,
                    "success": success,
                    "state_root": self.processor.get_state_root()
                })
                if not success:
                    return False
        return True
    
    def compare_replay(self, chain_a: List[Dict], chain_b: List[Dict]) -> Dict:
        """Compare two replay results"""
        # Save original state
        original_chain = self.processor.chain.copy() if hasattr(self.processor, 'chain') else []
        
        # Replay chain A
        self.replay_chain(chain_a)
        state_a = self.processor.get_state_root()
        
        # Reset
        if hasattr(self.processor, 'chain'):
            self.processor.chain = original_chain.copy()
        
        # Replay chain B
        self.replay_chain(chain_b)
        state_b = self.processor.get_state_root()
        
        return {
            "chain_a_root": state_a,
            "chain_b_root": state_b,
            "identical": state_a == state_b
        }

class AdversarialFuzzer:
    """Generate adversarial inputs for testing"""
    
    @staticmethod
    def random_tx() -> Dict:
        """Generate random transaction"""
        import random
        return {
            "from": f"addr_{random.randint(1, 1000)}",
            "to": f"addr_{random.randint(1, 1000)}",
            "amount": random.randint(1, 10000),
            "gas": random.randint(21000, 100000),
            "gas_price": random.randint(1, 100),
            "nonce": random.randint(0, 10)
        }
    
    @staticmethod
    def corrupted_block(original: Dict) -> Dict:
        """Create corrupted version of block"""
        import copy
        corrupted = copy.deepcopy(original)
        import random
        fields = list(corrupted.keys())
        if fields:
            field = random.choice(fields)
            if isinstance(corrupted[field], int):
                corrupted[field] += random.randint(-100, 100)
            elif isinstance(corrupted[field], str):
                corrupted[field] = corrupted[field][::-1]
        return corrupted
    
    @staticmethod
    def generate_spam_tx(count: int) -> List[Dict]:
        """Generate spam transactions"""
        spam = []
        for i in range(count):
            spam.append({
                "hash": f"spam_{i}_{hashlib.sha256(str(i).encode()).hexdigest()[:8]}",
                "from": f"spammer_{i % 10}",
                "to": f"victim_{i % 100}",
                "amount": 1,
                "gas": 21000,
                "gas_price": 0,
                "nonce": i
            })
        return spam

class ConsensusSimulator:
    """Simulate consensus under adversarial conditions"""
    
    def __init__(self, beacon, slashing):
        self.beacon = beacon
        self.slashing = slashing
        self.simulation_log = []
    
    def simulate_attestation_delay(self, block_hash: str, validator: str, delay_seconds: int):
        """Simulate delayed attestations"""
        import time
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        self.beacon.add_attestation(block_hash, validator)
        self.simulation_log.append({
            "type": "delayed_attestation",
            "block": block_hash,
            "validator": validator,
            "delay": delay_seconds
        })
    
    def simulate_double_vote(self, validator: str, block_a: str, block_b: str, epoch: int):
        """Simulate validator double voting"""
        self.slashing.record_vote(validator, block_a, epoch)
        self.slashing.record_vote(validator, block_b, epoch)
        self.simulation_log.append({
            "type": "double_vote",
            "validator": validator,
            "blocks": [block_a, block_b],
            "epoch": epoch
        })
    
    def get_simulation_log(self) -> List[Dict]:
        return self.simulation_log
