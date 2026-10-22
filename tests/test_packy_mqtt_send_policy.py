"""Offline tests for explicit, per-network, session-bound send consent."""
import configparser
import unittest
from packy_mqtt_send_policy import check_send_permission
from second_network import add_test_network


class SendPolicyTests(unittest.TestCase):
    def setUp(self):
        add_test_network(self)

    def test_default_denied(self):
        config = configparser.ConfigParser()
        for network in ('ctmesh', 'testnet'):
            self.assertFalse(check_send_permission(config, network).allowed)

    def test_demo_always_denied(self):
        config = configparser.ConfigParser()
        config['mqtt_ctmesh'] = {'enabled': 'true', 'allow_publish': 'true'}
        self.assertFalse(check_send_permission(config, 'ctmesh', demo=True, session_confirmed=True).allowed)

    def test_each_network_requires_explicit_consent(self):
        config = configparser.ConfigParser()
        config['mqtt_ctmesh'] = {'enabled': 'true', 'allow_publish': 'true'}
        config['mqtt_testnet'] = {'enabled': 'true'}
        self.assertFalse(check_send_permission(config, 'ctmesh', session_confirmed=False).allowed)
        self.assertTrue(check_send_permission(config, 'ctmesh', session_confirmed=True).allowed)
        self.assertFalse(check_send_permission(config, 'testnet', session_confirmed=True).allowed)

    def test_unknown_network_denied(self):
        self.assertFalse(check_send_permission(configparser.ConfigParser(), 'other', session_confirmed=True).allowed)


if __name__ == '__main__':
    unittest.main()
