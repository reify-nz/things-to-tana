import requests
import json
from typing import List, Dict, Any
from config import TANA_LOCAL_API_ENDPOINT, DEBUG
from models import TanaNode

class TanaLocalClient:
    """
    Client for Tana Local API (MCP protocol).
    
    The Local API runs on the Tana desktop app and doesn't require API tokens.
    Enable it in Tana desktop: Settings > Tana Labs > Local API/MCP server (Alpha)
    """
    def __init__(self, endpoint: str = TANA_LOCAL_API_ENDPOINT):
        self.endpoint = endpoint

    def send_nodes(self, nodes: List[TanaNode], target_node_id: str = 'INBOX') -> bool:
        """
        Sends a list of TanaNodes to the Tana Local API.
        
        Args:
            nodes: List of TanaNode objects to send
            target_node_id: Target node ID (default: 'INBOX')
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not nodes:
            return True

        headers = {
            "Content-Type": "application/json"
        }

        # Convert TanaNodes to API payload format
        nodes_payload = [node.to_api_payload() for node in nodes]

        payload = {
            "targetNodeId": target_node_id,
            "nodes": nodes_payload
        }

        # Debug: Print payload only if DEBUG=true
        if DEBUG:
            print(f"\n[DEBUG] Sending payload to Tana Local API:")
            print(json.dumps(payload, indent=2))
            print(f"[DEBUG] Target node: {target_node_id}")
            print(f"[DEBUG] Number of nodes: {len(nodes_payload)}")
            print(f"[DEBUG] Endpoint: {self.endpoint}\n")

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            print(f"✓ Successfully sent {len(nodes)} nodes to Tana via Local API ({target_node_id}).")
            return True
        except requests.exceptions.ConnectionError as e:
            print(f"✗ Error: Cannot connect to Tana Local API at {self.endpoint}")
            print(f"  Make sure:")
            print(f"  1. Tana desktop app is running")
            print(f"  2. Local API is enabled in Tana: Settings > Tana Labs > Local API/MCP server (Alpha)")
            print(f"  3. The local API is running on the correct port (default: http://localhost:8262)")
            if DEBUG:
                print(f"  Connection error details: {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Error sending data to Tana Local API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response status: {e.response.status_code}")
                print(f"  Response content: {e.response.text}")
            return False
