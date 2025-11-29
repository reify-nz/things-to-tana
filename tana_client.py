import requests
import json
from typing import List, Dict, Any
from config import TANA_API_TOKEN, TANA_API_ENDPOINT
from models import TanaNode

class TanaClient:
    def __init__(self, api_token: str = TANA_API_TOKEN):
        self.api_token = api_token
        self.endpoint = TANA_API_ENDPOINT

    def send_nodes(self, nodes: List[TanaNode], target_node_id: str = 'INBOX') -> bool:
        """
        Sends a list of TanaNodes to the Tana Input API.
        """
        if not nodes:
            return True

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        # Convert TanaNodes to API payload format
        nodes_payload = [node.to_api_payload() for node in nodes]

        payload = {
            "targetNodeId": target_node_id,
            "nodes": nodes_payload
        }

        # Debug: Print payload
        print(f"\n[DEBUG] Sending payload to Tana API:")
        print(json.dumps(payload, indent=2))
        print(f"[DEBUG] Target node: {target_node_id}")
        print(f"[DEBUG] Number of nodes: {len(nodes_payload)}\n")

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            print(f"Successfully sent {len(nodes)} nodes to Tana ({target_node_id}).")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to Tana: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return False
