"""No-network tests for per-network MQTT packet deduplication."""
import unittest
from packy_mqtt_dedupe import PacketDeduplicator
from second_network import add_test_network


class PacketDedupeTests(unittest.TestCase):
    def setUp(self):
        add_test_network(self)

    def test_duplicate_and_network_isolation(self):
        cache = PacketDeduplicator()
        self.assertFalse(cache.duplicate('ctmesh', 'test', 123, 7))
        self.assertTrue(cache.duplicate('ctmesh', 'test', 123, 7))
        self.assertFalse(cache.duplicate('testnet', 'test', 123, 7))
        self.assertFalse(cache.duplicate('ctmesh', 'other', 123, 7))

    def test_expiry_and_bounded_size(self):
        now = [0]
        cache = PacketDeduplicator(max_entries=2, ttl_seconds=10, clock=lambda: now[0])
        self.assertFalse(cache.duplicate('ctmesh', 'test', 1, 1))
        now[0] = 11
        self.assertFalse(cache.duplicate('ctmesh', 'test', 1, 1))
        cache.duplicate('ctmesh', 'test', 2, 2)
        cache.duplicate('ctmesh', 'test', 3, 3)
        self.assertLessEqual(len(cache._seen), 2)

    def test_invalid_identity_not_cached(self):
        cache = PacketDeduplicator()
        self.assertFalse(cache.duplicate('ctmesh', 'test', 0, 1))
        self.assertFalse(cache.duplicate('ctmesh', 'test', 0, 1))


if __name__ == '__main__':
    unittest.main()
