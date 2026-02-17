import pytest
from unittest.mock import patch, MagicMock, Mock
import requests
from tana_local_client import TanaLocalClient
from models import TanaNode


class TestTanaLocalClient:
    """Tests for TanaLocalClient class"""

    def test_init_default_endpoint(self):
        """Test that TanaLocalClient initializes with default endpoint"""
        client = TanaLocalClient()
        assert "localhost:8262" in client.endpoint
        assert "/mcp/addToNodeV2" in client.endpoint

    def test_init_custom_endpoint(self):
        """Test that TanaLocalClient can use custom endpoint"""
        custom_endpoint = "http://localhost:9999/custom/endpoint"
        client = TanaLocalClient(endpoint=custom_endpoint)
        assert client.endpoint == custom_endpoint

    @patch('tana_local_client.requests.post')
    def test_send_nodes_success(self, mock_post):
        """Test successful node sending via local API"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Create test nodes
        nodes = [
            TanaNode(name="Test Task 1"),
            TanaNode(name="Test Task 2")
        ]

        # Send nodes
        client = TanaLocalClient()
        result = client.send_nodes(nodes, target_node_id="INBOX")

        # Verify
        assert result == True
        mock_post.assert_called_once()
        
        # Check the payload structure
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert payload['targetNodeId'] == "INBOX"
        assert len(payload['nodes']) == 2

    @patch('tana_local_client.requests.post')
    def test_send_nodes_empty_list(self, mock_post):
        """Test that sending empty node list returns True without API call"""
        client = TanaLocalClient()
        result = client.send_nodes([], target_node_id="INBOX")
        
        assert result == True
        mock_post.assert_not_called()

    @patch('tana_local_client.requests.post')
    def test_send_nodes_connection_error(self, mock_post):
        """Test handling of connection errors"""
        mock_post.side_effect = requests.exceptions.ConnectionError("Cannot connect")

        nodes = [TanaNode(name="Test Task")]
        client = TanaLocalClient()
        result = client.send_nodes(nodes)

        assert result == False

    @patch('tana_local_client.requests.post')
    def test_send_nodes_http_error(self, mock_post):
        """Test handling of HTTP errors"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_post.return_value = mock_response

        nodes = [TanaNode(name="Test Task")]
        client = TanaLocalClient()
        result = client.send_nodes(nodes)

        assert result == False

    @patch('tana_local_client.requests.post')
    def test_send_nodes_with_supertag(self, mock_post):
        """Test sending nodes with supertags"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        node = TanaNode(name="Test Task")
        node.add_supertag("supertag-id-123")

        client = TanaLocalClient()
        result = client.send_nodes([node])

        assert result == True
        
        # Check supertag is in payload
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert len(payload['nodes'][0]['supertags']) == 1
        assert payload['nodes'][0]['supertags'][0]['id'] == "supertag-id-123"

    @patch('tana_local_client.DEBUG', True)
    @patch('tana_local_client.requests.post')
    def test_send_nodes_debug_mode(self, mock_post, capsys):
        """Test that debug mode prints payload information"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        nodes = [TanaNode(name="Debug Test")]
        client = TanaLocalClient()
        client.send_nodes(nodes)

        captured = capsys.readouterr()
        assert "[DEBUG]" in captured.out
        assert "Sending payload to Tana Local API" in captured.out


class TestSyncServiceWithLocalAPI:
    """Tests for SyncService with local API support"""

    @patch('sync_service.ThingsProvider')
    @patch('sync_service.HistoryManager')
    def test_sync_service_uses_local_client(self, mock_history, mock_provider):
        """Test that SyncService uses TanaLocalClient when use_local_api=True"""
        from sync_service import SyncService
        from tana_local_client import TanaLocalClient
        
        service = SyncService(use_local_api=True)
        
        # The client should be a TanaLocalClient instance
        assert isinstance(service.tana_client, TanaLocalClient)

    @patch('sync_service.ThingsProvider')
    @patch('sync_service.HistoryManager')
    def test_sync_service_uses_cloud_client_by_default(self, mock_history, mock_provider):
        """Test that SyncService uses TanaClient by default"""
        from sync_service import SyncService
        from tana_client import TanaClient
        
        service = SyncService(use_local_api=False)
        
        # The client should be a TanaClient instance
        assert isinstance(service.tana_client, TanaClient)


class TestCLILocalAPIFlag:
    """Tests for CLI --local-api flag"""

    @patch('things_to_tana.SyncService')
    def test_main_with_local_api_flag_today(self, mock_sync_service):
        """Test main() with --local-api flag for today scope"""
        import sys
        from things_to_tana import main
        
        mock_service_instance = MagicMock()
        mock_sync_service.return_value = mock_service_instance

        with patch.object(sys, 'argv', ['things_to_tana.py', 'today', '--local-api']):
            main()

        # Verify SyncService was called with use_local_api=True
        mock_sync_service.assert_called_once_with(use_local_api=True)
        mock_service_instance.sync_today.assert_called_once()

    @patch('things_to_tana.SyncService')
    def test_main_with_local_api_flag_inbox(self, mock_sync_service):
        """Test main() with --local-api flag for inbox scope"""
        import sys
        from things_to_tana import main
        
        mock_service_instance = MagicMock()
        mock_sync_service.return_value = mock_service_instance

        with patch.object(sys, 'argv', ['things_to_tana.py', 'inbox', '--local-api']):
            main()

        mock_sync_service.assert_called_once_with(use_local_api=True)
        mock_service_instance.sync_inbox.assert_called_once()

    @patch('things_to_tana.SyncService')
    def test_main_with_local_api_flag_all(self, mock_sync_service):
        """Test main() with --local-api flag for all scope"""
        import sys
        from things_to_tana import main
        
        mock_service_instance = MagicMock()
        mock_sync_service.return_value = mock_service_instance

        with patch.object(sys, 'argv', ['things_to_tana.py', 'all', '--local-api']):
            main()

        mock_sync_service.assert_called_once_with(use_local_api=True)
        # Both inbox and today should be called for 'all'
        mock_service_instance.sync_inbox.assert_called_once()
        mock_service_instance.sync_today.assert_called_once()

    @patch('things_to_tana.is_api_token_valid')
    @patch('things_to_tana.SyncService')
    def test_local_api_overrides_cloud_api(self, mock_sync_service, mock_is_valid):
        """Test that --local-api flag takes precedence over cloud API token"""
        import sys
        from things_to_tana import main
        
        # Even with valid token, local API should be used
        mock_is_valid.return_value = True
        mock_service_instance = MagicMock()
        mock_sync_service.return_value = mock_service_instance

        with patch.object(sys, 'argv', ['things_to_tana.py', 'today', '--local-api']):
            main()

        # Should use local API, not cloud API
        mock_sync_service.assert_called_once_with(use_local_api=True)

    @patch('things_to_tana.is_api_token_valid')
    @patch('things_to_tana.SyncService')
    def test_no_local_api_flag_uses_default_behavior(self, mock_sync_service, mock_is_valid):
        """Test that without --local-api, default behavior is preserved"""
        import sys
        from things_to_tana import main
        
        mock_is_valid.return_value = True
        mock_service_instance = MagicMock()
        mock_sync_service.return_value = mock_service_instance

        with patch.object(sys, 'argv', ['things_to_tana.py', 'today']):
            main()

        # Should use default (cloud API), not local API
        mock_sync_service.assert_called_once_with()
