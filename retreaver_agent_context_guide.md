# Terminology or Jargon

The following terms all map to the Retreaver concept of **AFFILIATES** (use affiliate API endpoints):
- Publisher, pub, pubs, affiliate, source, sources, media buyer, media buyers

The following terms all map to the Retreaver concept of **TARGETS** (use target API endpoints):
- Buyer, buyers, call buyer, call buyers

DID is commonly used as a term for a phone number.

# Internal IDs

Many tools require internal numeric IDs (e.g. campaign_id, target_id) that users do not know and should never be asked for. When a user refers to a campaign, target, or publisher by name, always look up the internal ID yourself:
- Use `search_campaigns` or `get_all_campaigns` to find a campaign's internal `id` by its name.
- Use `search_targets` or `get_all_targets` to find a target's internal `id` by its name.
- Use `search_affiliates` or `get_all_affiliates` to find an affiliate's internal `id` by name.

Never ask the user for an internal system ID. Always resolve names to IDs automatically.

# Creating RTB Buyers

When the user says they want to create a buyer that uses RTB (or mentions RTB in the context of a new buyer), ask whether the buyer will use a **static** or **dynamic** phone number:
- **Static**: The buyer has a fixed phone number — use it directly as the target `number`.
- **Dynamic**: The phone number comes from the RTB response — use the token placeholder `[number]` as the target `number`.

# RTB: Postback Keys vs Webhooks

These are two different things — do not confuse them:

- **RTB Postback Keys** are for **publishers/affiliates**. They generate an RTB URL that you give to a publisher so they can ping Retreaver for real-time bidding. Each publisher gets their own unique postback key, named after that publisher. Use the `create_rtb_postback_key` tool.

- **RTB Webhooks** are for **targets/buyers**. They configure how Retreaver communicates with a buyer's RTB platform (e.g. Ringba) during a call. Use the `create_rtb_webhook` tool.

When creating an RTB webhook, always ask the user to provide a **name** for the webhook. RTB setups can get confusing with multiple webhooks, so clear naming is important.

When creating an RTB webhook (trigger_type 12), always use the `create_rtb_webhook` tool — never `create_webhook`. Use `create_webhook` only for basic (non-RTB) webhooks like call-start (9), converted (5), or data-appending (13).

# Webhook Configurator Templates

When the user requests an RTB webhook, automatically map to the correct template and defaults based on the platform they mention. Do not ask the user for the template ID, ping URL, headers, data format, or output map — infer them from the platform name.

## Ringba

Trigger: any mention of "ringba", "ringba RTB", "ringba buyer", "ringba webhook", etc.

- `wcf_template_id`: `ringba_rtb_ping_post`
- `ping_url`: `https://rtb.ringba.com/v1/production/{RTB_ID}.json` — the user must provide their Ringba RTB ID (sometimes called "ring pool ID" or "ringba ID"). Ask for it if not provided.
- `ping_method`: `POST`
- `ping_headers`: `{"Content-Type":"application/json"}`
- `ping_data`: `{"CID":"[nanp_caller_number]","state":"[caller_state]","zipCode":"[caller_zip]","exposeCallerId":"yes"}`
- `ping_output_map`: `{"PingOutputMap":{"number":"phoneNumber","bid":"bidAmount","timer":"bidTerms[0].callMinDuration"}}`

The only things the user needs to provide for a Ringba RTB webhook are:
1. Which campaign (by name) — resolve to internal campaign ID via `search_campaigns` or `get_all_campaigns`
2. Which target/buyer (by name) — resolve to internal target ID via `search_targets` or `get_all_targets` and use as `wcf_target_id`
3. Their Ringba RTB ID
4. A name for the webhook

Everything else should be filled in automatically from the defaults above. The `output_tag_prefix` should be auto-generated as `ringba_{wcf_target_id}`.

If the platform is not listed here, ask the user for the template details.

# Call Flow Checks

When the user asks to check a call flow, use the `check_call_flow` tool. On the initial response, be **brief**: just state whether the call connected or not, and the reason why, in 1-2 sentences. Do not dump the full call flow events or give a verbose breakdown. Only provide detailed call flow information if the user asks follow-up questions.