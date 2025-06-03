import hashlib
import random
import json
import time
from typing import Dict, Any, Tuple
from dataclasses import dataclass, field

# === Simulated cryptographic primitives ===

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def generate_commitment(secret: str, nonce: str) -> str:
    return sha256(secret + nonce)

def generate_zk_proof(statement: str, witness: str) -> str:
    return sha256("PROOF|" + statement + "|" + witness)

def verify_zk_proof(statement: str, proof: str) -> bool:
    # Placeholder proof validation
    return proof.startswith(sha256("PROOF|" + statement)[:10])

# === MCP Message Struct ===

@dataclass
class MCPMessage:
    sender_id: str
    timestamp: float
    payload: Dict[str, Any]
    nonce: str
    signature: str = field(init=False)

    def __post_init__(self):
        self.signature = self._sign_message()

    def _sign_message(self) -> str:
        data = f"{self.sender_id}|{self.timestamp}|{json.dumps(self.payload)}|{self.nonce}"
        return sha256(data)

    def validate_signature(self) -> bool:
        expected_sig = self._sign_message()
        return self.signature == expected_sig

# === ZKMCP Gateway ===

class ZKMCPGateway:
    def __init__(self):
        self.registered_clients: Dict[str, str] = {}  # sender_id: public_key (simulated)
        self.message_log: Dict[str, MCPMessage] = {}  # message_id: message

    def register_client(self, sender_id: str, public_key: str):
        self.registered_clients[sender_id] = public_key
        print(f"[Gateway] Registered client: {sender_id}")

    def receive_message(self, message: MCPMessage) -> Tuple[bool, str]:
        if message.sender_id not in self.registered_clients:
            return False, "Unauthorized sender"

        if not message.validate_signature():
            return False, "Invalid signature"

        msg_id = sha256(message.signature + str(message.timestamp))
        self.message_log[msg_id] = message

        print(f"[Gateway] Message received and verified from {message.sender_id}")
        return True, msg_id

    def create_zk_proof_for_msg(self, msg_id: str) -> Tuple[str, str]:
        if msg_id not in self.message_log:
            raise ValueError("Message ID not found")

        msg = self.message_log[msg_id]
        statement = f"{msg.sender_id}|{msg.payload['action']}"
        witness = msg.signature

        proof = generate_zk_proof(statement, witness)
        return statement, proof

    def verify_external_proof(self, statement: str, proof: str) -> bool:
        is_valid = verify_zk_proof(statement, proof)
        status = "valid" if is_valid else "invalid"
        print(f"[Verifier] ZK Proof verification result: {status}")
        return is_valid

# === Simulated Birkini Node Usage ===

def simulate_birkini_protocol_flow():
    gateway = ZKMCPGateway()

    # Simulate client registration
    client_id = "birkini_node_01"
    pubkey = sha256("public_key_stub")
    gateway.register_client(client_id, pubkey)

    # Simulate message
    payload = {
        "action": "commit_data",
        "content": sha256("some_secure_content")
    }
    nonce = str(random.randint(100000, 999999))
    message = MCPMessage(sender_id=client_id, timestamp=time.time(), payload=payload, nonce=nonce)

    success, msg_id = gateway.receive_message(message)
    if not success:
        print(f"[Simulation] Message rejected: {msg_id}")
        return

    # ZKMCP Proof generation and verification
    statement, proof = gateway.create_zk_proof_for_msg(msg_id)
    gateway.verify_external_proof(statement, proof)

if __name__ == "__main__":
    simulate_birkini_protocol_flow()
