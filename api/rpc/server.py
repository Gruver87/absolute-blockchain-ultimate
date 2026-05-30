# api/rpc/server.py
import json
from typing import Dict, Any

class JSONRPCServer:
    """JSON-RPC API (Ethereum-style)"""
    
    def __init__(self, execution_client, consensus_client):
        self.execution = execution_client
        self.consensus = consensus_client
        self.methods = {
            "eth_blockNumber": self.eth_blockNumber,
            "eth_getBalance": self.eth_getBalance,
            "eth_sendRawTransaction": self.eth_sendRawTransaction,
            "eth_getTransactionCount": self.eth_getTransactionCount,
            "net_version": self.net_version,
            "web3_clientVersion": self.web3_clientVersion
        }
    
    def eth_blockNumber(self, params) -> str:
        return hex(0)
    
    def eth_getBalance(self, params) -> str:
        address = params[0] if params else None
        if address:
            balance = self.execution.state.get_balance(address)
            return hex(balance)
        return "0x0"
    
    def eth_getTransactionCount(self, params) -> str:
        address = params[0] if params else None
        if address:
            nonce = self.execution.state.get_nonce(address)
            return hex(nonce)
        return "0x0"
    
    def eth_sendRawTransaction(self, params) -> str:
        # Simplified — in production would decode and validate
        return "0x" + "0" * 64
    
    def net_version(self, params) -> str:
        return "1"
    
    def web3_clientVersion(self, params) -> str:
        return "AbsoluteBlockchain/v27.0"
    
    def handle_request(self, request: Dict) -> Dict:
        method = request.get("method")
        params = request.get("params", [])
        req_id = request.get("id")
        
        handler = self.methods.get(method)
        if handler:
            try:
                result = handler(params)
                return {"jsonrpc": "2.0", "result": result, "id": req_id}
            except Exception as e:
                return {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": req_id}
        
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}
