import os

# Tana API Token
# You can set this via environment variable or directly here (not recommended for sharing)
TANA_API_TOKEN = os.getenv("TANA_API_TOKEN", "YOUR_API_TOKEN_HERE")

# API Endpoint
TANA_API_ENDPOINT = "https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2"

# Node IDs
# 'INBOX' is a special ID for the Tana Inbox.
TANA_INBOX_NODE_ID = "INBOX"

# You can specify a specific node ID for "Today" items, or use 'INBOX' if you process them later.
# If you leave it as None, it might default to Inbox or you can set a specific node ID.
TANA_TODAY_NODE_ID = os.getenv("TANA_TODAY_NODE_ID", "INBOX") 

# Supertag to apply to synced tasks
# This should be the name of the supertag in Tana, e.g., #task
SUPERTAG_NAME = os.getenv("SUPERTAG_NAME", "task")
