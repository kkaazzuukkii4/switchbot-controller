import unittest
import service
from repository import SwitchNotExistError,GetSwitchError,UpdateStateError
from unittest.mock import patch
import json

class SwitchbotServiceTest(unittest.TestCase):
    def test_is_valid_format_when_format_is_valid_and_state_is_True(self):
        valid_format = {
            "switch_name": "test",
            "state": True,
            "location": "somwhere"
        }
        self.assertTrue(service.is_valid_format(valid_format))

    def test_is_valid_format_when_format_is_valid_and_state_is_False(self):
        valid_format = {
            "switch_name": "test",
            "state": False,
            "location": "somwhere"
        }
        self.assertTrue(service.is_valid_format(valid_format))

    def test_is_valid_format_when_format_is_invalid_because_switch_name_is_None(self):
        invalid_format = {
            "state": True,
            "location": "somwhere"
        }
        self.assertFalse(service.is_valid_format(invalid_format))

    def test_is_valid_format_when_format_is_invalid_because_state_is_None(self):
        invalid_format = {
            "switch_name": "something",
            "location": "somwhere"
        }
        self.assertFalse(service.is_valid_format(invalid_format))

    def test_is_valid_format_when_format_is_invalid_because_state_is_not_bool(self):
        invalid_format = {
            "switch_name": "something",
            "state": "aiueo",
            "location": "somwhere"
        }
        self.assertFalse(service.is_valid_format(invalid_format))

    @patch("switchbot.execute")
    @patch("state_repository.StateRepository")
    def test_exec_switchbot_not_call_switchbot_when_local_state_and_received_state_is_equality(self, mock_repository, mock_switchbot):
        mock_repository.get_data_by_switch_name.return_value = {
            "name": "test",
            "state": True,
            "mac": "aa:bb:cc:dd"
        }
        service.exec_switchbot(json.dumps({
            "switch_name": "test",
            "state": True,
            "location": "living"
        }), mock_repository)
        mock_repository.get_data_by_switch_name.assert_called_with("test")
        mock_switchbot.assert_not_called()

    @patch("switchbot.execute")
    @patch("state_repository.StateRepository")
    def test_exec_switchbot_call_switchbot_when_local_state_and_received_state_is_not_equality(self, mock_repository, mock_switchbot):
        mock_repository.get_data_by_switch_name.return_value = {
            "name": "test",
            "state": False,
            "mac": "aa:bb:cc:dd"
        }
        service.exec_switchbot(json.dumps({
            "switch_name": "test",
            "state": True,
            "location": "living"
        }), mock_repository)
        mock_repository.get_data_by_switch_name.assert_called_with("test")
        mock_repository.update_state_by_switch_name.assert_called_with("test", True)
        mock_switchbot.assert_called_with(mac="aa:bb:cc:dd",dev_type="Bot",cmd="Press")

    @patch("switchbot.execute")
    @patch("state_repository.StateRepository")
    def test_exec_switchbot_when_target_switch_is_not_registered(self,mock_repository, mock_switchbot):
        mock_repository.get_data_by_switch_name.side_effect=SwitchNotExistError
        service.exec_switchbot(json.dumps({
            "switch_name": "test",
            "state": True,
            "location": "living"
        }), mock_repository)
        mock_switchbot.assert_not_called()

    @patch("switchbot.execute")
    @patch("state_repository.StateRepository")
    def test_exec_switchbot_when_occur_get_data_unexpected_error(self,mock_repository, mock_switchbot):
        mock_repository.get_data_by_switch_name.side_effect=GetSwitchError
        service.exec_switchbot(json.dumps({
            "switch_name": "test",
            "state": True,
            "location": "living"
        }), mock_repository)
        mock_switchbot.assert_not_called()

    @patch("switchbot.execute")
    @patch("state_repository.StateRepository")
    def test_exec_switchbot_when_occur_update_data_unexpected_error(self,mock_repository, mock_switchbot):
        mock_repository.update_state_by_switch_name.side_effect = UpdateStateError
        mock_repository.get_data_by_switch_name.return_value = {
            "name": "test",
            "state": False,
            "mac": "aa:bb:cc:dd"
        }
        service.exec_switchbot(json.dumps({
            "switch_name": "test",
            "state": True,
            "location": "living"
        }), mock_repository)
        mock_switchbot.assert_called_with(mac="aa:bb:cc:dd", dev_type="Bot", cmd="Press")
        mock_repository.update_state_by_switch_name.assert_called_with("test", True)

if __name__ == "__main__":
    unittest.main()