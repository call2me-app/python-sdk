"""Call2Me API Client — Full API coverage."""

import httpx
from typing import Optional, Dict, Any, List


class Call2Me:
    """Call2Me API client.

    Usage:
        from call2me import Call2Me
        client = Call2Me(api_key="sk_call2me_...")
        agents = client.agents.list()
    """

    def __init__(self, api_key: str, base_url: str = "https://api.call2me.app"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=30,
        )
        self.agents = AgentsResource(self._http)
        self.calls = CallsResource(self._http)
        self.knowledge_bases = KnowledgeBaseResource(self._http)
        self.wallet = WalletResource(self._http)
        self.campaigns = CampaignsResource(self._http)
        self.schedules = SchedulesResource(self._http)
        self.phone_numbers = PhoneNumbersResource(self._http)
        self.sip_trunks = SipTrunksResource(self._http)
        self.api_keys = ApiKeysResource(self._http)
        self.users = UsersResource(self._http)
        self.widgets = WidgetsResource(self._http)
        self.voices = VoicesResource(self._http)
        self.chats = ChatsResource(self._http)
        self.payments = PaymentsResource(self._http)
        self.events = EventsResource(self._http)

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class _Resource:
    def __init__(self, http: httpx.Client):
        self._http = http

    def _get(self, path: str, **params) -> Any:
        r = self._http.get(path, params={k: v for k, v in params.items() if v is not None})
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, data: Dict = None) -> Any:
        r = self._http.post(path, json=data or {})
        r.raise_for_status()
        return r.json()

    def _patch(self, path: str, data: Dict = None) -> Any:
        r = self._http.patch(path, json=data or {})
        r.raise_for_status()
        return r.json()

    def _put(self, path: str, data: Dict = None) -> Any:
        r = self._http.put(path, json=data or {})
        r.raise_for_status()
        return r.json()

    def _delete(self, path: str) -> bool:
        r = self._http.delete(path)
        r.raise_for_status()
        return True

    def _post_file(self, path: str, file_path: str, field: str = "file") -> Any:
        with open(file_path, "rb") as f:
            r = self._http.post(path, files={field: f})
        r.raise_for_status()
        return r.json()


# ── Agents ──
class AgentsResource(_Resource):
    def list(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        return self._get("/v1/agents", limit=limit, offset=offset)

    def get(self, agent_id: str) -> Dict:
        return self._get(f"/v1/agents/{agent_id}")

    def create(self, agent_name: str, voice_id: str = "elevenlabs-selin",
               language: str = "tr-TR", system_prompt: str = "", **kwargs) -> Dict:
        data = {
            "agent_name": agent_name, "voice_id": voice_id, "language": language,
            "response_engine": {"type": "call2me-llm", "system_prompt": system_prompt,
                                "llm_model": kwargs.pop("model", "openrouter/auto")},
            **kwargs,
        }
        return self._post("/v1/agents", data)

    def update(self, agent_id: str, **kwargs) -> Dict:
        return self._patch(f"/v1/agents/{agent_id}", kwargs)

    def delete(self, agent_id: str) -> bool:
        return self._delete(f"/v1/agents/{agent_id}")

    def duplicate(self, agent_id: str) -> Dict:
        return self._post(f"/v1/agents/{agent_id}/duplicate")

    def stats(self, agent_id: str, days: int = 30) -> Dict:
        return self._get(f"/v1/agents/{agent_id}/stats", days=days)

    def global_stats(self) -> Dict:
        return self._get("/v1/agents/stats/global")


# ── Calls ──
class CallsResource(_Resource):
    def list(self, limit: int = 50, offset: int = 0, agent_id: str = None) -> List[Dict]:
        return self._get("/v1/calls", limit=limit, offset=offset, agent_id=agent_id)

    def get(self, call_id: str) -> Dict:
        return self._get(f"/v1/calls/{call_id}")

    def end(self, call_id: str) -> Dict:
        return self._post(f"/v1/calls/{call_id}/end")

    def recording(self, call_id: str) -> Dict:
        return self._get(f"/v1/calls/{call_id}/recording")


# ── Knowledge Base ──
class KnowledgeBaseResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/knowledge-base")

    def get(self, kb_id: str) -> Dict:
        return self._get(f"/v1/knowledge-base/{kb_id}")

    def create(self, name: str, description: str = "") -> Dict:
        return self._post("/v1/knowledge-base", {"name": name, "description": description})

    def delete(self, kb_id: str) -> bool:
        return self._delete(f"/v1/knowledge-base/{kb_id}")

    def add_source(self, kb_id: str, source_type: str, content: str, name: str = "") -> Dict:
        return self._post(f"/v1/knowledge-base/{kb_id}/sources", {
            "type": source_type, "content": content, "name": name,
        })

    def query(self, kb_id: str, query: str, top_k: int = 5) -> Dict:
        return self._post(f"/v1/knowledge-base/{kb_id}/query", {"query": query, "top_k": top_k})


# ── Wallet ──
class WalletResource(_Resource):
    def balance(self) -> Dict:
        return self._get("/v1/wallet/balance")

    def transactions(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        return self._get("/v1/wallet/transactions", limit=limit, offset=offset)

    def analytics(self, days: int = 30) -> Dict:
        return self._get("/v1/wallet/analytics", days=days)

    def pricing(self) -> Dict:
        return self._get("/v1/wallet/pricing")


# ── Campaigns ──
class CampaignsResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/campaigns")

    def get(self, campaign_id: str) -> Dict:
        return self._get(f"/v1/campaigns/{campaign_id}")

    def create(self, name: str, agent_id: str, from_number: str, **kwargs) -> Dict:
        return self._post("/v1/campaigns", {"name": name, "agent_id": agent_id, "from_number": from_number, **kwargs})

    def update(self, campaign_id: str, **kwargs) -> Dict:
        return self._patch(f"/v1/campaigns/{campaign_id}", kwargs)

    def delete(self, campaign_id: str) -> bool:
        return self._delete(f"/v1/campaigns/{campaign_id}")

    def upload_csv(self, campaign_id: str, file_path: str) -> Dict:
        return self._post_file(f"/v1/campaigns/{campaign_id}/upload-csv", file_path)

    def action(self, campaign_id: str, action: str) -> Dict:
        """action: start, pause, resume, cancel"""
        return self._post(f"/v1/campaigns/{campaign_id}/action", {"action": action})

    def start(self, campaign_id: str) -> Dict:
        return self.action(campaign_id, "start")

    def pause(self, campaign_id: str) -> Dict:
        return self.action(campaign_id, "pause")

    def resume(self, campaign_id: str) -> Dict:
        return self.action(campaign_id, "resume")

    def cancel(self, campaign_id: str) -> Dict:
        return self.action(campaign_id, "cancel")

    def contacts(self, campaign_id: str) -> List[Dict]:
        return self._get(f"/v1/campaigns/{campaign_id}/contacts")


# ── Schedules ──
class SchedulesResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/schedules")

    def get(self, schedule_id: str) -> Dict:
        return self._get(f"/v1/schedules/{schedule_id}")

    def create(self, agent_id: str, phone_number: str, scheduled_at: str, **kwargs) -> Dict:
        return self._post("/v1/schedules", {
            "agent_id": agent_id, "phone_number": phone_number,
            "scheduled_at": scheduled_at, **kwargs,
        })

    def update(self, schedule_id: str, **kwargs) -> Dict:
        return self._patch(f"/v1/schedules/{schedule_id}", kwargs)

    def delete(self, schedule_id: str) -> bool:
        return self._delete(f"/v1/schedules/{schedule_id}")

    def cancel(self, schedule_id: str) -> Dict:
        return self._post(f"/v1/schedules/{schedule_id}/cancel")


# ── Phone Numbers ──
class PhoneNumbersResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/phone-numbers")

    def get(self, number: str) -> Dict:
        return self._get(f"/v1/phone-numbers/{number}")

    def create(self, phone_number: str, **kwargs) -> Dict:
        return self._post("/v1/phone-numbers", {"phone_number": phone_number, **kwargs})

    def update(self, number: str, **kwargs) -> Dict:
        return self._patch(f"/v1/phone-numbers/{number}", kwargs)

    def delete(self, number: str) -> bool:
        return self._delete(f"/v1/phone-numbers/{number}")

    def bind_agent(self, number: str, agent_id: str) -> Dict:
        return self._post(f"/v1/phone-numbers/{number}/bind", {"agent_id": agent_id})

    def unbind_agent(self, number: str) -> Dict:
        return self._post(f"/v1/phone-numbers/{number}/unbind")


# ── SIP Trunks ──
class SipTrunksResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/sip-trunks")

    def get(self, trunk_id: str) -> Dict:
        return self._get(f"/v1/sip-trunks/{trunk_id}")

    def create(self, name: str, sip_server: str, sip_username: str, sip_password: str, **kwargs) -> Dict:
        return self._post("/v1/sip-trunks", {
            "name": name, "sip_server": sip_server,
            "sip_username": sip_username, "sip_password": sip_password, **kwargs,
        })

    def update(self, trunk_id: str, **kwargs) -> Dict:
        return self._patch(f"/v1/sip-trunks/{trunk_id}", kwargs)

    def delete(self, trunk_id: str) -> bool:
        return self._delete(f"/v1/sip-trunks/{trunk_id}")

    def test(self, trunk_id: str) -> Dict:
        return self._post(f"/v1/sip-trunks/{trunk_id}/test")


# ── API Keys ──
class ApiKeysResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/api-keys")

    def create(self, name: str, **kwargs) -> Dict:
        return self._post("/v1/api-keys", {"name": name, **kwargs})

    def revoke(self, key_id: str) -> Dict:
        return self._patch(f"/v1/api-keys/{key_id}/revoke")

    def delete(self, key_id: str) -> bool:
        return self._delete(f"/v1/api-keys/{key_id}")

    def usage(self, key_id: str) -> Dict:
        return self._get(f"/v1/api-keys/{key_id}/usage")


# ── Users ──
class UsersResource(_Resource):
    def me(self) -> Dict:
        return self._get("/v1/users/me")

    def update(self, **kwargs) -> Dict:
        return self._patch("/v1/users/me", kwargs)

    def stats(self) -> Dict:
        return self._get("/v1/users/me/stats")

    def usage(self, days: int = 30) -> Dict:
        return self._get("/v1/users/me/usage", days=days)

    def daily_usage(self, days: int = 30) -> List[Dict]:
        return self._get("/v1/users/me/usage/daily", days=days)

    def branding(self) -> Dict:
        return self._get("/v1/users/me/branding")

    def update_branding(self, **kwargs) -> Dict:
        return self._put("/v1/users/me/branding", kwargs)

    def tenant_members(self, page: int = 1, per_page: int = 20) -> Dict:
        return self._get("/v1/users/me/tenant/members", page=page, per_page=per_page)


# ── Widgets ──
class WidgetsResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/widgets")

    def get(self, widget_id: str) -> Dict:
        return self._get(f"/v1/widgets/{widget_id}")

    def create(self, agent_id: str, name: str = "", **kwargs) -> Dict:
        return self._post("/v1/widgets", {"agent_id": agent_id, "name": name, **kwargs})

    def update(self, widget_id: str, **kwargs) -> Dict:
        return self._patch(f"/v1/widgets/{widget_id}", kwargs)

    def delete(self, widget_id: str) -> bool:
        return self._delete(f"/v1/widgets/{widget_id}")

    def chat(self, widget_id: str, message: str, visitor_id: str = None) -> Dict:
        return self._post(f"/v1/widgets/{widget_id}/chat", {
            "message": message, "visitor_id": visitor_id,
        })


# ── Voices ──
class VoicesResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/voices")

    def providers(self) -> List[Dict]:
        return self._get("/v1/voices/providers")


# ── Chats ──
class ChatsResource(_Resource):
    def list(self, limit: int = 50) -> List[Dict]:
        return self._get("/v1/chats", limit=limit)

    def get(self, session_id: str) -> Dict:
        return self._get(f"/v1/chats/{session_id}")

    def send_message(self, session_id: str, content: str, model: str = None) -> Dict:
        data = {"content": content}
        if model:
            data["model"] = model
        return self._post(f"/v1/chats/{session_id}/messages", data)


# ── Payments ──
class PaymentsResource(_Resource):
    def checkout(self, amount: float, currency: str = "USD") -> Dict:
        return self._post("/v1/payments/checkout", {"amount": amount, "currency": currency})

    def history(self, limit: int = 50) -> List[Dict]:
        return self._get("/v1/payments/history", limit=limit)

    def saved_cards(self) -> List[Dict]:
        return self._get("/v1/payments/saved-cards")

    def auto_charge(self) -> Dict:
        return self._get("/v1/payments/auto-charge")

    def update_auto_charge(self, enabled: bool, threshold: float = None, amount: float = None) -> Dict:
        data = {"enabled": enabled}
        if threshold is not None:
            data["threshold"] = threshold
        if amount is not None:
            data["charge_amount"] = amount
        return self._put("/v1/payments/auto-charge", data)


class EventsResource(_Resource):
    """Report custom events (errors, auth, payments, custom).

    The ingest endpoint is public — it doesn't require the SDK's API key
    — but a key is still sent so authenticated events inherit the user's
    higher rate limit (100/min vs 10/min for anon).
    """
    def report(self, type: str, message: str, source: str = "api",
               severity: str = None, meta: Dict = None,
               tenant: str = None, session_id: str = None,
               fingerprint: str = None) -> Dict:
        body = {
            "type": type,
            "source": source,
            "message": message,
        }
        if severity: body["severity"] = severity
        if tenant: body["tenant"] = tenant
        if session_id: body["session_id"] = session_id
        if fingerprint: body["fingerprint"] = fingerprint
        if meta: body["meta"] = meta
        return self._post("/v1/events", body)

    def query(self, severity: str = None, type: str = None,
              fingerprint: str = None, hours: int = 24, limit: int = 50) -> Dict:
        """Admin-only — JWT required rather than API key. SDK users with
        admin rights can call it if they authenticate via the Authorization
        header directly."""
        params = {"hours": hours, "limit": limit}
        if severity: params["severity"] = severity
        if type: params["type"] = type
        if fingerprint: params["fingerprint"] = fingerprint
        return self._get("/v1/events", **params)
