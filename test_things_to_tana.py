import pytest
from unittest.mock import patch, MagicMock, call
import sys
from things_to_tana import is_api_token_valid, main, convert_task_to_node


# --- Tests for is_api_token_valid() ---

@patch('things_to_tana.TANA_API_TOKEN', 'valid-token-12345')
def test_is_api_token_valid_with_valid_token():
    """Test that a valid token returns True"""
    assert is_api_token_valid() == True


@patch('things_to_tana.TANA_API_TOKEN', 'YOUR_API_TOKEN_HERE')
def test_is_api_token_valid_with_placeholder():
    """Test that placeholder token returns False"""
    assert is_api_token_valid() == False


@patch('things_to_tana.TANA_API_TOKEN', '')
def test_is_api_token_valid_with_empty_string():
    """Test that empty string returns False"""
    assert is_api_token_valid() == False


@patch('things_to_tana.TANA_API_TOKEN', None)
def test_is_api_token_valid_with_none():
    """Test that None returns False"""
    assert is_api_token_valid() == False


# --- Tests for main() - API Sync Mode ---

@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.SyncService')
def test_main_api_mode_today(mock_sync_service, mock_is_valid):
    """Test main() uses API sync for 'today' scope when token is valid"""
    mock_is_valid.return_value = True
    mock_service_instance = MagicMock()
    mock_sync_service.return_value = mock_service_instance

    # Simulate command line args
    with patch.object(sys, 'argv', ['things_to_tana.py', 'today']):
        main()

    # Verify SyncService was instantiated and sync_today was called
    mock_sync_service.assert_called_once()
    mock_service_instance.sync_today.assert_called_once()
    mock_service_instance.sync_inbox.assert_not_called()


@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.SyncService')
def test_main_api_mode_inbox(mock_sync_service, mock_is_valid):
    """Test main() uses API sync for 'inbox' scope when token is valid"""
    mock_is_valid.return_value = True
    mock_service_instance = MagicMock()
    mock_sync_service.return_value = mock_service_instance

    with patch.object(sys, 'argv', ['things_to_tana.py', 'inbox']):
        main()

    mock_service_instance.sync_inbox.assert_called_once()
    mock_service_instance.sync_today.assert_not_called()


@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.SyncService')
def test_main_api_mode_all(mock_sync_service, mock_is_valid):
    """Test main() uses API sync for 'all' scope when token is valid"""
    mock_is_valid.return_value = True
    mock_service_instance = MagicMock()
    mock_sync_service.return_value = mock_service_instance

    with patch.object(sys, 'argv', ['things_to_tana.py', 'all']):
        main()

    # Both inbox and today should be called for 'all'
    mock_service_instance.sync_inbox.assert_called_once()
    mock_service_instance.sync_today.assert_called_once()


@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.SyncService')
def test_main_api_mode_default_scope(mock_sync_service, mock_is_valid):
    """Test main() defaults to 'today' scope when no arg provided"""
    mock_is_valid.return_value = True
    mock_service_instance = MagicMock()
    mock_sync_service.return_value = mock_service_instance

    with patch.object(sys, 'argv', ['things_to_tana.py']):
        main()

    mock_service_instance.sync_today.assert_called_once()


# --- Tests for main() - Clipboard Sync Mode ---

@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.get_things_tasks')
@patch('things_to_tana.to_tana_paste')
@patch('things_to_tana.pyperclip.copy')
def test_main_clipboard_mode_success(mock_copy, mock_to_tana_paste, mock_get_tasks, mock_is_valid):
    """Test main() uses clipboard sync when no valid token"""
    mock_is_valid.return_value = False
    mock_get_tasks.return_value = [
        {'title': 'Task 1', 'type': 'to-do', 'uuid': '123'},
        {'title': 'Task 2', 'type': 'to-do', 'uuid': '456'}
    ]
    mock_to_tana_paste.return_value = "%%tana%%\n- Task 1\n- Task 2"

    with patch.object(sys, 'argv', ['things_to_tana.py', 'today']):
        main()

    # Verify clipboard flow
    mock_get_tasks.assert_called_once_with("today")
    mock_to_tana_paste.assert_called_once()
    mock_copy.assert_called_once_with("%%tana%%\n- Task 1\n- Task 2")


@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.get_things_tasks')
def test_main_clipboard_mode_no_tasks(mock_get_tasks, mock_is_valid):
    """Test main() handles empty task list in clipboard mode"""
    mock_is_valid.return_value = False
    mock_get_tasks.return_value = []

    with patch.object(sys, 'argv', ['things_to_tana.py', 'today']):
        main()

    # Should return early, no clipboard copy
    mock_get_tasks.assert_called_once_with("today")


@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.get_things_tasks')
def test_main_clipboard_mode_error_handling(mock_get_tasks, mock_is_valid):
    """Test main() handles Things API errors gracefully"""
    mock_is_valid.return_value = False
    mock_get_tasks.side_effect = Exception("Things database error")

    with patch.object(sys, 'argv', ['things_to_tana.py', 'today']):
        main()  # Should not raise, just print error

    mock_get_tasks.assert_called_once_with("today")


@patch('things_to_tana.is_api_token_valid')
@patch('things_to_tana.get_things_tasks')
@patch('things_to_tana.to_tana_paste')
@patch('things_to_tana.pyperclip.copy')
def test_main_clipboard_mode_filters_projects(mock_copy, mock_to_tana_paste, mock_get_tasks, mock_is_valid):
    """Test main() filters out projects in clipboard mode"""
    mock_is_valid.return_value = False
    mock_get_tasks.return_value = [
        {'title': 'Task 1', 'type': 'to-do', 'uuid': '123'},
        {'title': 'Project 1', 'type': 'project', 'uuid': '456'},
        {'title': 'Task 2', 'type': 'to-do', 'uuid': '789'}
    ]
    mock_to_tana_paste.return_value = "%%tana%%\n- Task 1\n- Task 2"

    with patch.object(sys, 'argv', ['things_to_tana.py', 'today']):
        main()

    # to_tana_paste should be called with 2 nodes (projects filtered out)
    call_args = mock_to_tana_paste.call_args[0][0]
    assert len(call_args) == 2


# --- Tests for convert_task_to_node() ---

def test_convert_task_to_node_basic():
    """Test basic task conversion"""
    task = {
        'title': 'Test Task',
        'notes': '',
        'tags': [],
        'due_date': None,
        'checklist': [],
        'status': ''
    }

    node = convert_task_to_node(task)

    assert node.text == 'Test Task'
    assert node.checked == False


def test_convert_task_to_node_with_due_date():
    """Test task conversion with due date"""
    task = {
        'title': 'Test Task',
        'notes': '',
        'tags': [],
        'due_date': '2025-11-30',
        'checklist': [],
        'status': ''
    }

    node = convert_task_to_node(task)

    assert '[[date:2025-11-30]]' in node.text


def test_convert_task_to_node_completed():
    """Test completed task conversion"""
    task = {
        'title': 'Completed Task',
        'notes': '',
        'tags': [],
        'due_date': None,
        'checklist': [],
        'status': 'completed'
    }

    node = convert_task_to_node(task)

    assert node.checked == True


def test_convert_task_to_node_canceled():
    """Test canceled task conversion"""
    task = {
        'title': 'Canceled Task',
        'notes': '',
        'tags': [],
        'due_date': None,
        'checklist': [],
        'status': 'canceled'
    }

    node = convert_task_to_node(task)

    assert node.checked == True
    assert '#canceled' in node.text


@patch('things_to_tana.SUPERTAG_NAME', 'task')
def test_convert_task_to_node_with_supertag():
    """Test task conversion with configured supertag"""
    task = {
        'title': 'Test Task',
        'notes': '',
        'tags': [],
        'due_date': None,
        'checklist': [],
        'status': ''
    }

    node = convert_task_to_node(task)

    assert 'task' in node.supertags


def test_convert_task_to_node_with_tags():
    """Test task conversion with tags"""
    task = {
        'title': 'Test Task',
        'notes': '',
        'tags': ['urgent', 'work'],
        'due_date': None,
        'checklist': [],
        'status': ''
    }

    node = convert_task_to_node(task)

    assert 'urgent' in node.supertags
    assert 'work' in node.supertags


def test_convert_task_to_node_with_notes():
    """Test task conversion with notes"""
    task = {
        'title': 'Test Task',
        'notes': 'First line\nSecond line\n\nThird line',
        'tags': [],
        'due_date': None,
        'checklist': [],
        'status': ''
    }

    node = convert_task_to_node(task)

    # Should have 3 children (empty line skipped)
    assert len(node.children) == 3
    assert node.children[0].text == 'First line'
    assert node.children[1].text == 'Second line'
    assert node.children[2].text == 'Third line'


def test_convert_task_to_node_with_checklist():
    """Test task conversion with checklist items"""
    task = {
        'title': 'Test Task',
        'notes': '',
        'tags': [],
        'due_date': None,
        'checklist': [
            {'title': 'Item 1', 'status': 'completed'},
            {'title': 'Item 2', 'status': ''}
        ],
        'status': ''
    }

    node = convert_task_to_node(task)

    assert len(node.children) == 2
    assert node.children[0].text == 'Item 1'
    assert node.children[0].checked == True
    assert node.children[1].text == 'Item 2'
    assert node.children[1].checked == False
