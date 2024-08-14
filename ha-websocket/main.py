import websocket
import json
import ssl

def create_token():
    HA_URL = env.get("HA_URL", "hass:8123")
    socket_connection = websocket.create_connection(f"ws://{HA_URL}/api/websocket", sslopt={'cert_reqs': ssl.CERT_NONE})
    socket_response = socket_connection.recv()
    result = json.loads(socket_response)

    auth = None
    if result["type"] == "auth_required":
        auth = json.dumps({
            "type": "auth",
            "api_password": env.get("LEGACY_API_PASSWORD")
        })
        socket_connection.send(auth)
        auth_response = socket_connection.recv()

    token_request = json.dumps({
      "id": 11,
      "type": "auth/long_lived_access_token",
      "client_name": "GPS Logger",
      "client_icon": "no icon",
      "lifespan": 365
    })
    socket_connection.send(token_request)
    token_response = socket_connection.recv()
    q = json.loads(token_response)

    return q["result"]

create_token()
