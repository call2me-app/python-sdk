# Call2Me Python SDK

The official Python SDK for [Call2Me](https://call2me.app) — the AI voice agent platform.

Build, deploy, and manage AI voice agents that handle real phone calls, extract data, and take automated actions.

[![PyPI](https://img.shields.io/pypi/v/call2me)](https://pypi.org/project/call2me/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- **Voice Agents** — Create and manage AI agents with custom voices and personalities
- **Phone & Web Calls** — Handle inbound/outbound calls via SIP or browser
- **30+ AI Models** — GPT, Claude, Gemini, DeepSeek, Llama, and more
- **Knowledge Base** — RAG-powered answers from your documents
- **Campaigns** — Bulk outbound calling at scale
- **Scheduled Calls** — Book follow-up calls automatically
- **Post-Call Intelligence** — Extract structured data from every conversation
- **Multi-Language** — Turkish, English, German, French, Spanish, Arabic

## Installation

```bash
pip install call2me
```

Requires Python 3.8+

## Getting Your API Key

1. Sign up at [dashboard.call2me.app](https://dashboard.call2me.app/signup) — you get **$10 free credits**
2. Go to **API Keys** in the dashboard
3. Click **Create API Key** and copy it

## Quick Start

```python
from call2me import Call2Me

client = Call2Me(api_key="sk_call2me_...")

# Create a voice agent
agent = client.agents.create(
    agent_name="Customer Support",
    voice_id="elevenlabs-selin",
    language="tr-TR",
    system_prompt="You are a friendly customer support agent for our company."
)
print(f"Agent created: {agent['agent_id']}")
```

## Usage Examples

### List Agents

```python
agents = client.agents.list()
for agent in agents:
    print(f"{agent['agent_id']} — {agent['agent_name']} ({agent['status']})")
```

### Get Call History

```python
calls = client.calls.list(limit=10)
for call in calls:
    print(f"{call['call_id']} | {call['direction']} | {call['call_status']} | {call.get('duration_ms', 0)}ms")
```

### Knowledge Base

```python
# Create a knowledge base
kb = client.knowledge_bases.create(
    name="Product FAQ",
    description="Frequently asked questions about our products"
)

# Query it
results = client.knowledge_bases.query(kb['id'], "What is the return policy?")
```

### Campaigns

```python
# Create a campaign
campaign = client.campaigns.create(
    name="Spring Sale Outreach",
    agent_id="agent_abc123",
    from_number="+908501234567"
)

# Start calling
client.campaigns.start(campaign['id'])
```

### Scheduled Calls

```python
# Schedule a follow-up call
schedule = client.schedules.create(
    agent_id="agent_abc123",
    phone_number="+905551234567",
    scheduled_at="2026-04-15T10:00:00+03:00",
    timezone="Europe/Istanbul"
)
```

### Check Balance

```python
balance = client.wallet.balance()
print(f"Balance: ${balance['balance_usd']}")

# Transaction history
txns = client.wallet.transactions(limit=5)
```

## API Reference

| Resource | Methods |
|----------|---------|
| `client.agents` | `list()`, `get(id)`, `create(...)`, `update(id, ...)`, `delete(id)`, `duplicate(id)` |
| `client.calls` | `list()`, `get(id)` |
| `client.knowledge_bases` | `list()`, `create(...)`, `query(id, query)` |
| `client.wallet` | `balance()`, `transactions()` |
| `client.campaigns` | `list()`, `create(...)`, `start(id)`, `pause(id)` |
| `client.schedules` | `list()`, `create(...)` |

## Configuration

```python
# Custom base URL (for self-hosted or testing)
client = Call2Me(
    api_key="sk_call2me_...",
    base_url="https://your-api.example.com"
)

# Context manager (auto-close)
with Call2Me(api_key="sk_call2me_...") as client:
    agents = client.agents.list()
```

## Documentation

- **Full API Docs**: [call2me.app/docs](https://call2me.app/docs)
- **Guides**: [call2me.app/guides](https://call2me.app/guides)
- **Pricing**: [call2me.app/pricing](https://call2me.app/pricing)

## Support

- Email: [support@call2me.app](mailto:support@call2me.app)
- Website: [call2me.app](https://call2me.app)

## License

MIT — see [LICENSE](LICENSE) for details.
