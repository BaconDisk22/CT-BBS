"""Offline tests for MQTT connection lifecycle without broker access."""
import configparser
import unittest
from packy_dual_mqtt import DualMQTTMonitors
from second_network import add_test_network


class FakeClient:
    def __init__(self):
        self.started = 0
        self.stopped = 0
        self.disconnected = 0
    def tls_set(self, **kwargs): pass
    def reconnect_delay_set(self, **kwargs): pass
    def connect_async(self, host, port, keepalive): pass
    def loop_start(self): self.started += 1
    def disconnect(self): self.disconnected += 1
    def loop_stop(self): self.stopped += 1


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        add_test_network(self)

    def test_duplicate_connect_does_not_start_second_loop(self):
        config = configparser.ConfigParser()
        config['mqtt_ctmesh'] = {'enabled': 'true', 'topic': 'msh/US/2/e/test'}
        manager = DualMQTTMonitors(config)
        client = FakeClient()
        self.assertTrue(manager.connect('ctmesh', factory=lambda: client))
        self.assertTrue(manager.connect('ctmesh', factory=lambda: self.fail('duplicate client')))
        self.assertEqual(client.started, 1)
        manager.stop('ctmesh')
        self.assertEqual(client.stopped, 1)
        self.assertEqual(client.disconnected, 1)

    def test_stop_all_keeps_networks_independent(self):
        config = configparser.ConfigParser()
        for section in ('mqtt_ctmesh', 'mqtt_testnet'):
            config[section] = {'enabled': 'true', 'topic': 'msh/US/2/e/test'}
        manager = DualMQTTMonitors(config)
        clients = {'ctmesh': FakeClient(), 'testnet': FakeClient()}
        for name in clients:
            self.assertTrue(manager.connect(name, factory=lambda n=name: clients[n]))
        manager.stop()
        self.assertEqual(clients['ctmesh'].stopped, 1)
        self.assertEqual(clients['testnet'].stopped, 1)


if __name__ == '__main__':
    unittest.main()
