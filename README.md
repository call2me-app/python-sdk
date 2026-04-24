# Call2Me Python SDK

The official Python SDK for [Call2Me](https://call2me.app) — the AI voice agent platform.

Build, deploy, and manage AI voice agents that handle real phone calls, extract data, and take automated actions.

[![PyPI](https://img.shields.io/pypi/v/call2me)](https://pypi.org/project/call2me/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- **15 API Resources** — Full coverage of the Call2Me REST API
- **Voice Agents** — Create agents with 30+ AI models and custom voices
- **Phone & Web Calls** — Inbound/outbound via SIP, browser, or chat widget
- **Campaigns** — Bulk outbound calling with CSV upload
- **Scheduled Calls** — Book follow-ups at specific dates
- **Post-Call Intelligence** — Auto-extract data and trigger actions
- **Knowledge Base** — RAG-powered answers from your documents
- **White-Label** — Custom branding, domain, and tenant management
- **Payments** — Checkout, saved cards, auto-charge

## Installation

```bash
pip install call2me
```

Requires Python 3.8+

## Getting Your API Key

1. Sign up at [dashboard.call2me.app](https://dashboard.call2me.app/signup) — you get **$10 free credits**
2. Go to **API Keys** in the dashboard
3. Click **Create API Key** and copy your `sk_call2me_...` key

## Quick Start

```python
from call2me import Call2Me

client = Call2Me(api_key="sk_call2me_...")

# Create an agent
agent = client.agents.create(
    agent_name="Sales Agent",
    voice_id="elevenlabs-selin",
    language="tr-TR",
    system_prompt="You are a friendly sales agent."
)
print(f"Agent: {agent['agent_id']}")

# List calls
for call in client.calls.list():
    print(f"{call['call_id']} — {call['call_status']}")

# Check balance
print(f"Balance: ${client.wallet.balance()['balance_usd']}")
```

## Full API Reference

### Agents
```python
client.agents.list(limit=100, offset=0)
client.agents.get("agent_id")
client.agents.create(agent_name="My Agent", voice_id="elevenlabs-selin", system_prompt="...")
client.agents.update("agent_id", agent_name="New Name")
client.agents.delete("agent_id")
client.agents.duplicate("agent_id")
client.agents.stats("agent_id", days=30)
client.agents.global_stats()
```

### Calls
```python
client.calls.list(limit=50, agent_id="agent_id")
client.calls.get("call_id")
client.calls.end("call_id")
client.calls.recording("call_id")
```

### Knowledge Base
```python
client.knowledge_bases.list()
client.knowledge_bases.get("kb_id")
client.knowledge_bases.create(name="FAQ", description="Product FAQ")
client.knowledge_bases.delete("kb_id")
client.knowledge_bases.add_source("kb_id", source_type="text", content="...", name="intro")
client.knowledge_bases.query("kb_id", "What is the return policy?", top_k=5)
```

### Campaigns
```python
client.campaigns.list()
client.campaigns.get("campaign_id")
client.campaigns.create(name="Spring Sale", agent_id="agent_id", from_number="+908501234567")
client.campaigns.update("campaign_id", name="Updated")
client.campaigns.delete("campaign_id")
client.campaigns.upload_csv("campaign_id", "/path/to/contacts.csv")
client.campaigns.start("campaign_id")
client.campaigns.pause("campaign_id")
client.campaigns.resume("campaign_id")
client.campaigns.cancel("campaign_id")
client.campaigns.contacts("campaign_id")
```

### Scheduled Calls
```python
client.schedules.list()
client.schedules.get("schedule_id")
client.schedules.create(agent_id="agent_id", phone_number="+905551234567", scheduled_at="2026-04-15T10:00:00+03:00", timezone="Europe/Istanbul")
client.schedules.update("schedule_id", scheduled_at="2026-04-16T14:00:00+03:00")
client.schedules.delete("schedule_id")
client.schedules.cancel("schedule_id")
```

### Phone Numbers
```python
client.phone_numbers.list()
client.phone_numbers.get("+908501234567")
client.phone_numbers.create(phone_number="+908501234567", trunk_id="trunk_id")
client.phone_numbers.update("+908501234567", display_name="Main Line")
client.phone_numbers.delete("+908501234567")
client.phone_numbers.bind_agent("+908501234567", "agent_id")
client.phone_numbers.unbind_agent("+908501234567")
```

### SIP Trunks
```python
client.sip_trunks.list()
client.sip_trunks.get("trunk_id")
client.sip_trunks.create(name="My Trunk", sip_server="sip.provider.com", sip_username="user", sip_password="pass")
client.sip_trunks.update("trunk_id", name="Updated")
client.sip_trunks.delete("trunk_id")
client.sip_trunks.test("trunk_id")
```

### Wallet & Billing
```python
client.wallet.balance()
client.wallet.transactions(limit=50, offset=0)
client.wallet.analytics(days=30)
client.wallet.pricing()
```

### Payments
```python
client.payments.checkout(amount=50.0, currency="USD")
client.payments.history(limit=50)
client.payments.saved_cards()
client.payments.auto_charge()
client.payments.update_auto_charge(enabled=True, threshold=5.0, amount=50.0)
```

### API Keys
```python
client.api_keys.list()
client.api_keys.create(name="Production Key")
client.api_keys.revoke("key_id")
client.api_keys.delete("key_id")
client.api_keys.usage("key_id")
```

### Users & Branding
```python
client.users.me()
client.users.update(full_name="John Doe", company_name="Acme Inc")
client.users.stats()
client.users.usage(days=30)
client.users.daily_usage(days=30)
client.users.branding()
client.users.update_branding(app_name="My Platform", primary_color="#6366f1")
client.users.tenant_members(page=1, per_page=20)
```

### Widgets
```python
client.widgets.list()
client.widgets.get("widget_id")
client.widgets.create(agent_id="agent_id", name="Support Widget")
client.widgets.update("widget_id", welcome_message="Hi!")
client.widgets.delete("widget_id")
client.widgets.chat("widget_id", "Hello, I need help")
```

### Voices
```python
client.voices.list()
client.voices.providers()
```

### Chats
```python
client.chats.list(limit=50)
client.chats.get("session_id")
client.chats.send_message("session_id", "Hello!", model="openrouter/auto")
```

### Events

Forward application errors and business events to the Call2Me
observability pipeline. The POST endpoint is public; sending the API
key lifts your per-minute ceiling from 10 (anon) to 100.

```python
client.events.report(
    type="payment_failed",
    source="api",
    message="Paddle rejected the webhook",
    severity="error",
    meta={"payment_id": "pay_abc", "provider": "paddle"},
)

# Admin-only query over archived (error+) events:
client.events.query(severity="error", hours=24)
```

Common `type` values: `js_error`, `unhandled_rejection`, `http_5xx`,
`auth_login`, `auth_signup`, `payment_success`, `payment_failed`,
`call_started`, `call_ended`, `call_failed`, `agent_crash`.

## Error Handling

```python
import httpx

try:
    agent = client.agents.get("invalid_id")
except httpx.HTTPStatusError as e:
    print(f"Error {e.response.status_code}: {e.response.json()}")
```

## Links

- **Website**: [call2me.app](https://call2me.app)
- **Dashboard**: [dashboard.call2me.app](https://dashboard.call2me.app)
- **API Docs**: [call2me.app/docs](https://call2me.app/docs)
- **Guides**: [call2me.app/guides](https://call2me.app/guides)
- **GitHub**: [github.com/call2me-app/python-sdk](https://github.com/call2me-app/python-sdk)
- **Support**: [support@call2me.app](mailto:support@call2me.app)

## Changelog

### 1.3.1 (2026-04-24)
- README — publish the 1.3.0 events-resource documentation to PyPI
  (the 1.3.0 upload shipped the pre-release README by accident).

### 1.3.0 (2026-04-24)
- Add `events` resource — `client.events.report()` and `.query()` for
  forwarding errors and business events to the observability pipeline.
- Published via PyPI Trusted Publishing (OIDC, no API token).

### 1.2.0
- All 14 resources, campaigns, schedules, widgets.

## License

MIT
