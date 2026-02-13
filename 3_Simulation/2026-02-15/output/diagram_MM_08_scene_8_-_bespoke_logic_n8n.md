# n8n Bespoke Automation Flow

**Type:** sequence
**Generated:** 2026-02-13T21:26:51.052479

```mermaid
sequenceDiagram
    participant Wife as Wife
    participant UI as GitHub Pages UI
    participant N8N as n8n Workflow
    participant Router as Home Router

    Wife->>UI: Toggle internet off for Kid
    UI->>N8N: Trigger webhook
    N8N->>N8N: Lookup MAC address
    N8N->>Router: Apply firewall rule
    Router->>N8N: Confirm block
    N8N->>UI: Status updated
```
