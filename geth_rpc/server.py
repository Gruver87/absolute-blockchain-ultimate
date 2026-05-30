# geth_rpc/server.py
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

class JSONRPCServer:
    """JSON-RPC API (Ethereum style)"""
    
    def __init__(self, node, port: int = 8545):
        self.node = node
        self.port = port
        self.server = None
    
    def start(self):
        """Start JSON-RPC server"""
        handler = self._create_handler()
        self.server = HTTPServer(("0.0.0.0", self.port), handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        print(f"🚀 JSON-RPC server started on port {self.port}")
    
    def _create_handler(self):
        node = self.node
        
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                
                try:
                    req = json.loads(body.decode())
                    result = self._handle_request(req, node)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
            
            def _handle_request(self, req: Dict, node) -> Dict:
                method = req.get("method")
                params = req.get("params", [])
                req_id = req.get("id")
                
                handlers = {
                    "eth_blockNumber": lambda: hex(node.processor.get_chain_height()),
                    "eth_getBalance": lambda: hex(node.state.get_balance(params[0]) if params else "0x0"),
                    "eth_sendRawTransaction": lambda: "0x" + "0" * 64,
                    "web3_clientVersion": lambda: "AbsoluteBlockchain/v30.0",
                    "net_version": lambda: "1"
                }
                
                result = handlers.get(method, lambda: None)()
                if result is None:
                    return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}
                
                return {"jsonrpc": "2.0", "result": result, "id": req_id}
            
            def log_message(self, format, *args):
                pass
        
        return Handler
    
    def stop(self):
        if self.server:
            self.server.shutdown()
