"""The app ships exactly one MQTT network: CTMesh."""
import configparser
import unittest

from packy_dual_mqtt import NETWORKS, DualMQTTMonitors
from packy_mqtt_event_queue import MQTTEventQueue
from packy_mqtt_feed import NETWORK_LABELS
from packy_mqtt_pipeline import MQTTMessagePipeline
from packy_mqtt_send_policy import check_send_permission


class ShippedNetworkTests(unittest.TestCase):
    def test_only_ctmesh_is_registered(self):
        self.assertEqual(NETWORK_LABELS, {'ctmesh': 'CTMesh'})
        self.assertEqual(set(NETWORKS), {'ctmesh'})
        self.assertEqual(set(DualMQTTMonitors(configparser.ConfigParser()).monitors), {'ctmesh'})

    def test_removed_networks_are_unknown_everywhere(self):
        config = configparser.ConfigParser()
        for network in ('valleymesh', 'sjmesh', 'centralnj'):
            with self.subTest(network=network):
                self.assertEqual(MQTTMessagePipeline().process(network, b'').reason, 'Unknown network')
                self.assertFalse(MQTTEventQueue().push(network, object()))
                self.assertEqual(check_send_permission(config, network).reason, 'Unknown network')


if __name__ == '__main__':
    unittest.main()
