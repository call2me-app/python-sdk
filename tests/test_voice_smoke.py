"""voice_sessions.create doğru endpoint'e POST atıyor mu (offline mock)."""

import httpx

from call2me.client import Call2Me, VoiceSessionsResource


def test_voice_session_create_posts_to_endpoint():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["body"] = request.content.decode()
        return httpx.Response(
            200,
            json={"token": "t", "url": "wss://x", "room_name": "agent_a_1", "session_limit_sec": 3600},
        )

    client = Call2Me("sk_test")
    client._http = httpx.Client(
        base_url="https://api.call2me.app",
        transport=httpx.MockTransport(handler),
        headers={"Authorization": "Bearer sk_test"},
    )
    client.voice_sessions = VoiceSessionsResource(client._http)

    out = client.voice_sessions.create("agent_abc", context={"name": "Ada"})
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/v1/voice/sessions")
    assert "agent_abc" in captured["body"]
    assert out["room_name"] == "agent_a_1"
