# CTMesh: Intel Mac verification checklist

These desktop MQTT sessions are **receive-only activity monitors**, not a two-way Meshtastic transport. No broker publish, radio transmission, or cross-network bridge is implemented here.

## Before testing
- Build and launch the current Intel Mac release candidate.
- Save separate broker hostname, port, TLS setting, authorized exact topic and credentials for each network in Settings. Never put credentials in an issue, screenshot, or CI log.
- Leave both profiles disabled unless you are authorized to subscribe.
- Use only the narrowest authorized topic: an exact topic, or one channel from every gateway (`msh/<region>/2/e/<channel>/+`). No other wildcards.
- Do not enable auto-connect until manual connectivity is verified.

## Manual connection
1. Enable CTMesh only, save, restart the app, and click **Connect CTMesh**.
2. Verify the CTMesh status.
3. With authorized test traffic on the selected topic, check CTMesh MQTT RX increments. Radio RX/TX counts must not change as a consequence.
4. Disconnect CTMesh and verify that it stops.
5. Disconnect broker networking temporarily. Verify status and reconnect behavior, without freezes or crashes.
6. Quit the app; the MQTT client loop should stop.

## Auto-connect and safety
- Set enabled=true and auto_connect=true for CTMesh. Restart and confirm it connects.
- Confirm enabled=false or auto_connect=false prevents automatic startup for that profile.
- Run Demo mode: no broker connection should be opened.
- Try an empty topic, a `#` topic, or a `+` anywhere but the gateway position: connection must be refused.
- Verify credentials never appear in diagnostics or screenshots.

## Release gate
Record the app build SHA, macOS version, broker-side permission, observed status and RX count, and any error messages. Do not claim live broker interoperability based only on offline tests. Two-way MQTT publishing remains out of scope.
