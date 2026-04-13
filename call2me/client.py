"""Call2Me API Client."""

import httpx
from typing import Optional, Dict, Any, List


class Call2Me:
    """Call2Me API client.

    Usage:
        from call2me import Call2Me

        client = Call2Me(api_key="sk_call2me_...")

        # Create agent
        agent = client.agents.create(
            agent_name="My Agent",
            voice_id="elevenlabs-selin",
            language="tr-TR",
            system_prompt="You are a helpful assistant."
        )

        # List agents
        agents = client.agents.list()

        # Get call history
        calls = client.calls.list()
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
        r = self._http.get(path, params=params)
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

    def _delete(self, path: str) -> bool:
        r = self._http.delete(path)
        r.raise_for_status()
        return r.status_code == 204


class AgentsResource(_Resource):
    def list(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        return self._get("/v1/agents", limit=limit, offset=offset)

    def get(self, agent_id: str) -> Dict:
        return self._get(f"/v1/agents/{agent_id}")

    def create(self, agent_name: str, voice_id: str = "elevenlabs-selin",
               language: str = "tr-TR", system_prompt: str = "", **kwargs) -> Dict:
        data = {
            "agent_name": agent_name,
            "voice_id": voice_id,
            "language": language,
            "response_engine": {
                "type": "call2me-llm",
                "system_prompt": system_prompt,
                "llm_model": kwargs.pop("model", "openrouter/auto"),
            },
            **kwargs,
        }
        return self._post("/v1/agents", data)

    def update(self, agent_id: str, **kwargs) -> Dict:
        return self._patch(f"/v1/agents/{agent_id}", kwargs)

    def delete(self, agent_id: str) -> bool:
        return self._delete(f"/v1/agents/{agent_id}")

    def duplicate(self, agent_id: str) -> Dict:
        return self._post(f"/v1/agents/{agent_id}/duplicate")


class CallsResource(_Resource):
    def list(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        return self._get("/v1/calls", limit=limit, offset=offset)

    def get(self, call_id: str) -> Dict:
        return self._get(f"/v1/calls/{call_id}")


class KnowledgeBaseResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/knowledge-base")

    def create(self, name: str, description: str = "") -> Dict:
        return self._post("/v1/knowledge-base", {"name": name, "description": description})

    def query(self, kb_id: str, query: str, top_k: int = 5) -> Dict:
        return self._post(f"/v1/knowledge-base/{kb_id}/query", {"query": query, "top_k": top_k})


class WalletResource(_Resource):
    def balance(self) -> Dict:
        return self._get("/v1/wallet/balance")

    def transactions(self, limit: int = 50) -> List[Dict]:
        return self._get("/v1/wallet/transactions", limit=limit)


class CampaignsResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/campaigns")

    def create(self, name: str, agent_id: str, from_number: str, **kwargs) -> Dict:
        return self._post("/v1/campaigns", {"name": name, "agent_id": agent_id, "from_number": from_number, **kwargs})

    def start(self, campaign_id: str) -> Dict:
        return self._post(f"/v1/campaigns/{campaign_id}/action", {"action": "start"})

    def pause(self, campaign_id: str) -> Dict:
        return self._post(f"/v1/campaigns/{campaign_id}/action", {"action": "pause"})


class SchedulesResource(_Resource):
    def list(self) -> List[Dict]:
        return self._get("/v1/schedules")

    def create(self, agent_id: str, phone_number: str, scheduled_at: str, **kwargs) -> Dict:
        return self._post("/v1/schedules", {
            "agent_id": agent_id, "phone_number": phone_number,
            "scheduled_at": scheduled_at, **kwargs,
        })
