"""Register a fake second MQTT network so isolation tests have two to compare.

The app ships with CTMesh only; these tests keep proving that networks stay
apart if a real second Connecticut network is ever added.
"""
from unittest.mock import patch

import packy_dual_mqtt
import packy_mqtt_feed


def add_test_network(case):
    """Add 'testnet' to the network registries for the rest of this test."""
    for registry, entry in ((packy_mqtt_feed.NETWORK_LABELS, {'testnet': 'TestNet'}),
                            (packy_dual_mqtt.NETWORKS, {'testnet': ('mqtt_testnet', 'mqtt.example.test')})):
        patcher = patch.dict(registry, entry)
        patcher.start()
        case.addCleanup(patcher.stop)
