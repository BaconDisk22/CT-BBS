"""Offline MQTT receive counter isolation and retained-message checks."""
import configparser
import unittest
from types import SimpleNamespace
from packy_dual_mqtt import DualMQTTMonitors
from second_network import add_test_network


class ReceiveIsolationTests(unittest.TestCase):
    def setUp(self):
        add_test_network(self)

    def test_receive_counts_are_independent(self):
        manager = DualMQTTMonitors(configparser.ConfigParser())
        central = manager.monitors['ctmesh']
        south = manager.monitors['testnet']
        message = SimpleNamespace(retain=False, topic='msh/US/2/e/test')
        central._message(None, None, message)
        central._message(None, None, message)
        south._message(None, None, message)
        self.assertEqual(manager.snapshot()['ctmesh']['total'], 2)
        self.assertEqual(manager.snapshot()['testnet']['total'], 1)

    def test_retained_messages_are_not_new_activity(self):
        manager = DualMQTTMonitors(configparser.ConfigParser())
        monitor = manager.monitors['ctmesh']
        monitor._message(None, None, SimpleNamespace(retain=True, topic='msh/US/2/e/test'))
        self.assertEqual(monitor.snapshot()['total'], 0)

    def test_topic_counter_is_bounded(self):
        manager = DualMQTTMonitors(configparser.ConfigParser())
        monitor = manager.monitors['testnet']
        for i in range(1005):
            monitor._message(None, None, SimpleNamespace(retain=False, topic=f'msh/US/2/e/{i}'))
        data = monitor.snapshot()
        self.assertEqual(data['total'], 1005)
        self.assertEqual(data['overflow'], 5)
        self.assertLessEqual(len(monitor.counts), 1000)


if __name__ == '__main__':
    unittest.main()
