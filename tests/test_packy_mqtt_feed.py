"""Offline per-network MQTT feed and desktop drain tests."""
import configparser
import unittest
import packy_desktop as desktop
from packy_dual_mqtt import DualMQTTMonitors
from packy_mqtt_envelope import EnvelopeSummary
from packy_mqtt_feed import MeshFeed, FeedEntry, format_entry
from packy_mqtt_pipeline import ProcessingResult


def accepted(network='ctmesh', encrypted=True, portnum=None, from_id=0x7b, to_id=0xFFFFFFFF):
    summary = EnvelopeSummary('!12345678', 'LongFast', 7, from_id, to_id, encrypted, portnum)
    reason = 'Encrypted metadata only' if encrypted else 'Decoded metadata only'
    return ProcessingResult(True, reason, network, summary)


class FeedFormattingTests(unittest.TestCase):
    def test_encrypted_entry_shows_metadata_only(self):
        text = format_entry(FeedEntry(0, accepted()))
        self.assertIn('from !0000007b → broadcast', text)
        self.assertIn('ch LongFast', text)
        self.assertIn('via !12345678', text)
        self.assertIn('ENCRYPTED — not decrypted', text)

    def test_decoded_entry_names_port_but_not_content(self):
        text = format_entry(FeedEntry(0, accepted(encrypted=False, portnum=1, to_id=0x1c8)))
        self.assertIn('→ !000001c8', text)
        self.assertIn('TEXT_MESSAGE_APP — content not displayed', text)

    def test_rejection_shows_reason(self):
        text = format_entry(FeedEntry(0, ProcessingResult(False, 'Invalid MQTT envelope', 'valleymesh')))
        self.assertIn('REJECTED — Invalid MQTT envelope', text)


class MeshFeedTests(unittest.TestCase):
    def test_networks_are_kept_apart_and_newest_first(self):
        feed = MeshFeed(clock=iter(range(10)).__next__)
        feed.add('ctmesh', accepted(from_id=1))
        feed.add('ctmesh', accepted(from_id=2))
        feed.add('valleymesh', accepted('valleymesh', from_id=3))
        self.assertEqual([e.result.summary.from_id for e in feed.entries('ctmesh')], [2, 1])
        self.assertEqual([e.result.summary.from_id for e in feed.entries('valleymesh')], [3])

    def test_duplicates_and_unknown_networks_are_not_listed(self):
        feed = MeshFeed()
        self.assertFalse(feed.add('ctmesh', ProcessingResult(False, 'Duplicate packet', 'ctmesh')))
        self.assertFalse(feed.add('other', accepted()))
        self.assertEqual(feed.entries('ctmesh'), [])

    def test_feed_is_bounded(self):
        feed = MeshFeed(limit=3)
        for i in range(5):
            feed.add('valleymesh', accepted('valleymesh', from_id=i))
        self.assertEqual([e.result.summary.from_id for e in feed.entries('valleymesh')], [4, 3, 2])

    def test_empty_render_explains_how_to_connect(self):
        self.assertIn('No packets received', MeshFeed().render('valleymesh'))


class FakeText:
    """Minimal stand-in for a read-only Tk Text box."""
    def __init__(self):
        self.text, self.writes = '', 0
    def winfo_exists(self): return True
    def yview(self): return (0.0, 1.0)
    def yview_moveto(self, fraction): pass
    def configure(self, **kwargs): pass
    def get(self, start, end): return self.text
    def delete(self, start, end): self.text = ''
    def insert(self, index, text):
        self.text, self.writes = text, self.writes + 1


def envelope(packet_id=7):
    from meshtastic.protobuf import mqtt_pb2
    env = mqtt_pb2.ServiceEnvelope()
    env.gateway_id, env.channel_id = '!12345678', 'LongFast'
    env.packet.id = packet_id
    setattr(env.packet, 'from', 0x7b)
    env.packet.to = 0xFFFFFFFF
    env.packet.encrypted = b'ciphertext'
    return env.SerializeToString()


class DesktopDrainTests(unittest.TestCase):
    def app(self):
        app = desktop.PackyApp.__new__(desktop.PackyApp)
        app.mesh_feed = MeshFeed()
        app.dual_mqtt = DualMQTTMonitors(configparser.ConfigParser())
        app.wire_views = {name: FakeText() for name in ('ctmesh', 'valleymesh')}
        return app

    def test_drain_shows_packet_only_in_receiving_network(self):
        app = self.app()
        app.dual_mqtt.receive('ctmesh', envelope())
        app.drain_mqtt_events()
        self.assertIn('from !0000007b', app.wire_views['ctmesh'].text)
        self.assertNotIn('!0000007b', app.wire_views['valleymesh'].text)
        self.assertIn('Accepted 1', app.wire_views['ctmesh'].text)
        self.assertIn('Accepted 0', app.wire_views['valleymesh'].text)

    def test_unchanged_view_is_not_redrawn(self):
        app = self.app()
        app.drain_mqtt_events()
        app.drain_mqtt_events()
        self.assertEqual(app.wire_views['valleymesh'].writes, 1)

    def test_drain_without_open_wire_page_still_records(self):
        app = self.app()
        app.wire_views = {}
        app.dual_mqtt.receive('valleymesh', envelope())
        app.drain_mqtt_events()
        self.assertEqual(len(app.mesh_feed.entries('valleymesh')), 1)

    def test_drain_is_bounded_per_tick(self):
        app = self.app()
        for i in range(1, 80):
            app.dual_mqtt.receive('ctmesh', envelope(i))
        app.drain_mqtt_events()
        self.assertEqual(len(app.mesh_feed.entries('ctmesh')), 50)

    def test_no_broker_session_shows_not_connected(self):
        app = self.app()
        app.dual_mqtt = None
        app.drain_mqtt_events()
        self.assertIn('Connection: Not connected', app.wire_views['ctmesh'].text)


if __name__ == '__main__':
    unittest.main()
