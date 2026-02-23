"""MCP server exposing tools for the Retreaver API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .client import RetreaverClient

mcp = FastMCP("retreaver-write")
client = RetreaverClient()


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_target(
    number: str,
    name: str | None = None,
    tid: str | None = None,
    priority: int | None = None,
    weight: int | None = None,
    timeout_seconds: int | None = None,
    inband_signals: bool | None = None,
    timer_offset: int | None = None,
    send_digits: str | None = None,
    concurrency_cap: int | None = None,
    paused: bool | None = None,
    time_zone: str | None = None,
    sip_username: str | None = None,
    sip_password: str | None = None,
    business_hours_attributes: list[dict] | None = None,
) -> dict:
    """Create a new target (call destination).

    Parameters:
        number: Phone number (E.164, e.g. +18668987878), sip:user@domain.com,
            or a token placeholder in brackets (e.g. [number]).
        name: Display name for the target.
        tid: Your own custom target ID.
        priority: Routing priority — lower value is considered first (default 1).
        weight: Routing weight for load balancing among same-priority targets (default 1).
        timeout_seconds: Max seconds to ring before moving on (default 30).
        inband_signals: Enable in-band ringing detection.
        timer_offset: Offset any timers when routing to this target (seconds).
        send_digits: DTMF digits to send when answered (use "w" for 0.5s pause).
        concurrency_cap: Max simultaneous calls to this target.
        paused: If true, target is skipped during routing.
        time_zone: Time zone for business hours (e.g. "UTC", "Eastern Time (US & Canada)").
        sip_username: SIP auth username.
        sip_password: SIP auth password.
        business_hours_attributes: Array of business hours objects.
    """
    body: dict = {"number": number}
    for key, val in {
        "name": name, "tid": tid, "priority": priority, "weight": weight,
        "timeout_seconds": timeout_seconds, "inband_signals": inband_signals,
        "timer_offset": timer_offset, "send_digits": send_digits,
        "concurrency_cap": concurrency_cap, "paused": paused,
        "time_zone": time_zone, "sip_username": sip_username,
        "sip_password": sip_password,
    }.items():
        if val is not None:
            body[key] = val
    if business_hours_attributes is not None:
        body["business_hours_attributes"] = business_hours_attributes
    return await client.post("/targets.json", {"target": body})


@mcp.tool()
async def edit_target(
    target_id: int,
    number: str | None = None,
    name: str | None = None,
    tid: str | None = None,
    priority: int | None = None,
    weight: int | None = None,
    timeout_seconds: int | None = None,
    inband_signals: bool | None = None,
    timer_offset: int | None = None,
    send_digits: str | None = None,
    concurrency_cap: int | None = None,
    paused: bool | None = None,
    time_zone: str | None = None,
    sip_username: str | None = None,
    sip_password: str | None = None,
    business_hours_attributes: list[dict] | None = None,
) -> dict:
    """Edit an existing target by its internal ID. Only pass the fields you want to change.

    Parameters:
        target_id: Internal target ID to update.
        number: Phone number (E.164), sip:user@domain.com, or a token placeholder
            in brackets (e.g. [number]).
        name: Display name for the target.
        tid: Your own custom target ID.
        priority: Routing priority — lower value is considered first.
        weight: Routing weight for load balancing among same-priority targets.
        timeout_seconds: Max seconds to ring before moving on.
        inband_signals: Enable in-band ringing detection.
        timer_offset: Offset any timers when routing to this target (seconds).
        send_digits: DTMF digits to send when answered (use "w" for 0.5s pause).
        concurrency_cap: Max simultaneous calls to this target.
        paused: If true, target is skipped during routing.
        time_zone: Time zone for business hours.
        sip_username: SIP auth username.
        sip_password: SIP auth password.
        business_hours_attributes: Array of business hours objects.
    """
    body: dict = {}
    for key, val in {
        "number": number, "name": name, "tid": tid, "priority": priority,
        "weight": weight, "timeout_seconds": timeout_seconds,
        "inband_signals": inband_signals, "timer_offset": timer_offset,
        "send_digits": send_digits, "concurrency_cap": concurrency_cap,
        "paused": paused, "time_zone": time_zone,
        "sip_username": sip_username, "sip_password": sip_password,
    }.items():
        if val is not None:
            body[key] = val
    if business_hours_attributes is not None:
        body["business_hours_attributes"] = business_hours_attributes
    return await client.put(f"/targets/{target_id}.json", {"target": body})


@mcp.tool()
async def delete_target(target_id: int) -> dict | str:
    """Delete a target by its internal ID.

    Parameters:
        target_id: Internal target ID to delete.
    """
    return await client.delete(f"/targets/{target_id}.json")


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_campaign(
    cid: str,
    name: str | None = None,
    dedupe_seconds: int | None = None,
    affiliate_can_pull_number: bool | None = None,
    record_calls: bool | None = None,
    message: str | None = None,
    voice_gender: str | None = None,
    repeat: int | None = None,
    timers_attributes: list[dict] | None = None,
    menu_options_attributes: list[dict] | None = None,
) -> dict:
    """Create a new campaign.

    Parameters:
        cid: Your campaign ID — used to reference this campaign in the future.
        name: Campaign name for your reference.
        dedupe_seconds: Prevent repeat caller conversions within this many seconds (0 = disabled).
        affiliate_can_pull_number: Allow affiliates/publishers to pull tracking numbers.
        record_calls: Toggle call recording (default true).
        message: Text-to-speech greeting read to the caller.
        voice_gender: "Male" or "Female" for the TTS voice.
        repeat: Number of times to repeat the greeting (default 4).
        timers_attributes: Array of timer/webhook objects, e.g. [{"seconds": 0, "url": "..."}].
        menu_options_attributes: Array of menu options, e.g. [{"option": "1", "target_number": "+1..."}].
    """
    body: dict = {"cid": cid}
    for key, val in {
        "name": name, "dedupe_seconds": dedupe_seconds,
        "affiliate_can_pull_number": affiliate_can_pull_number,
        "record_calls": record_calls, "message": message,
        "voice_gender": voice_gender, "repeat": repeat,
    }.items():
        if val is not None:
            body[key] = val
    if timers_attributes is not None:
        body["timers_attributes"] = timers_attributes
    if menu_options_attributes is not None:
        body["menu_options_attributes"] = menu_options_attributes
    return await client.post("/campaigns.json", {"campaign": body})


@mcp.tool()
async def edit_campaign(
    cid: str,
    name: str | None = None,
    dedupe_seconds: int | None = None,
    affiliate_can_pull_number: bool | None = None,
    record_calls: bool | None = None,
    message: str | None = None,
    voice_gender: str | None = None,
    repeat: int | None = None,
    timers_attributes: list[dict] | None = None,
    menu_options_attributes: list[dict] | None = None,
) -> dict:
    """Edit an existing campaign by CID. Only pass the fields you want to change.

    Parameters:
        cid: Campaign ID to update.
        name: Campaign name.
        dedupe_seconds: Prevent repeat caller conversions within this many seconds (0 = disabled).
        affiliate_can_pull_number: Allow affiliates/publishers to pull tracking numbers.
        record_calls: Toggle call recording.
        message: Text-to-speech greeting read to the caller.
        voice_gender: "Male" or "Female" for the TTS voice.
        repeat: Number of times to repeat the greeting.
        timers_attributes: Array of timer/webhook objects.
        menu_options_attributes: Array of menu options.
    """
    body: dict = {}
    for key, val in {
        "name": name, "dedupe_seconds": dedupe_seconds,
        "affiliate_can_pull_number": affiliate_can_pull_number,
        "record_calls": record_calls, "message": message,
        "voice_gender": voice_gender, "repeat": repeat,
    }.items():
        if val is not None:
            body[key] = val
    if timers_attributes is not None:
        body["timers_attributes"] = timers_attributes
    if menu_options_attributes is not None:
        body["menu_options_attributes"] = menu_options_attributes
    return await client.put(f"/campaigns/cid/{cid}.json", {"campaign": body})


@mcp.tool()
async def delete_campaign(cid: str) -> dict | str:
    """Delete a campaign by its CID.

    Parameters:
        cid: Campaign ID to delete.
    """
    return await client.delete(f"/campaigns/cid/{cid}.json")


# ---------------------------------------------------------------------------
# Publishers (Affiliates)
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_publisher(
    afid: str,
    first_name: str | None = None,
    last_name: str | None = None,
    company_name: str | None = None,
) -> dict:
    """Create a new publisher (affiliate/source).

    Parameters:
        afid: Publisher ID — should align with any external tracking systems.
        first_name: Publisher's first name.
        last_name: Publisher's last name.
        company_name: Publisher's company name.
    """
    body: dict = {"afid": afid}
    if first_name is not None:
        body["first_name"] = first_name
    if last_name is not None:
        body["last_name"] = last_name
    if company_name is not None:
        body["company_name"] = company_name
    return await client.post("/affiliates.json", {"affiliate": body})


@mcp.tool()
async def edit_publisher(
    afid: str,
    first_name: str | None = None,
    last_name: str | None = None,
    company_name: str | None = None,
) -> dict:
    """Edit an existing publisher (affiliate/source) by AFID. Only pass the fields you want to change.

    Parameters:
        afid: Publisher ID to update.
        first_name: Publisher's first name.
        last_name: Publisher's last name.
        company_name: Publisher's company name.
    """
    body: dict = {}
    if first_name is not None:
        body["first_name"] = first_name
    if last_name is not None:
        body["last_name"] = last_name
    if company_name is not None:
        body["company_name"] = company_name
    return await client.put(f"/affiliates/afid/{afid}.json", {"affiliate": body})


@mcp.tool()
async def delete_publisher(afid: str) -> dict | str:
    """Delete a publisher (affiliate/source) by AFID.

    Parameters:
        afid: Publisher ID to delete.
    """
    return await client.delete(f"/affiliates/afid/{afid}.json")


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_number(
    cid: str,
    afid: str,
    number_type: str = "Toll-free",
    desired_text: str | None = None,
    country: str | None = None,
    sid: str | None = None,
) -> dict:
    """Create (provision) a new phone number.

    Parameters:
        cid: Campaign ID (user-set CID) this number belongs to. Campaign must exist first.
        afid: Affiliate/publisher ID (AFID) this number belongs to. Will create affiliate if not found.
        number_type: "Toll-free" or "Local" (default "Toll-free").
        desired_text: Attempt to get a number containing this word (vanity number).
        country: For Local numbers only, 2-character country code (default "US").
        sid: SubID this number belongs to.
    """
    body: dict = {"type": number_type, "afid": afid, "cid": cid}
    if desired_text is not None:
        body["desired_text"] = desired_text
    if country is not None:
        body["country"] = country
    if sid is not None:
        body["sid"] = sid
    return await client.post("/numbers.json", {"number": body})


@mcp.tool()
async def edit_number(
    number_id: int,
    afid: str | None = None,
    cid: str | None = None,
    sid: str | None = None,
) -> dict:
    """Update an existing number by its internal ID. Only pass fields you want to change.

    Parameters:
        number_id: Internal number ID.
        afid: Reassign to a different affiliate/publisher.
        cid: Reassign to a different campaign.
        sid: Update the SubID.
    """
    body: dict = {}
    if afid is not None:
        body["afid"] = afid
    if cid is not None:
        body["cid"] = cid
    if sid is not None:
        body["sid"] = sid
    return await client.put(f"/numbers/{number_id}.json", {"number": body})


@mcp.tool()
async def delete_number(number_id: int) -> dict | str:
    """Delete a number by its internal ID. Number will be deprovisioned within 24 hours.

    Parameters:
        number_id: Internal number ID to delete.
    """
    return await client.delete(f"/numbers/{number_id}.json")


# ---------------------------------------------------------------------------
# RTB Postback Keys
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_rtb_postback_key(
    campaign_id: int,
    name: str | None = None,
    tag_prefix: str | None = None,
    ttl_seconds: int | None = None,
    timeout: float | None = None,
    inbound_number: str | None = None,
    return_dba: bool | None = None,
    add_to_caps_on_status_reserved: bool | None = None,
    route_only_to_reserved_target: bool | None = None,
    allow_no_caller_number: bool | None = None,
    paused: bool | None = None,
    claim_percent_threshold: int | None = None,
    blocked_inbound_percent: int | None = None,
    ping_shield_outbound_count_limit: int | None = None,
    ping_shield_outbound_ms_limit: int | None = None,
) -> dict:
    """Create an RTB postback key for a campaign. Returns the RTB URL to give to publishers.

    Parameters:
        campaign_id: Internal campaign ID (not CID).
        name: Display name for this RTB key.
        tag_prefix: Prefix for tags created by this RTB integration.
        ttl_seconds: How long the RTB reservation lasts (default 30).
        timeout: HTTP timeout in seconds for the RTB ping (default 3.0).
        inbound_number: Specific inbound number to use for RTB calls.
        return_dba: If true, return doing-business-as info in the RTB response.
        add_to_caps_on_status_reserved: Count reserved calls toward concurrency caps.
        route_only_to_reserved_target: Only route to the target reserved by RTB.
        allow_no_caller_number: Allow RTB pings without a caller number.
        paused: If true, this RTB key is disabled.
        claim_percent_threshold: Minimum claim percentage to accept (default 10).
        blocked_inbound_percent: Percentage of inbound calls to block (default 50).
        ping_shield_outbound_count_limit: Max outbound pings for ping shield.
        ping_shield_outbound_ms_limit: Max milliseconds for ping shield.
    """
    body: dict = {
        "action": "rtb",
        "name": name or "",
        "tag_prefix": tag_prefix or "",
        "ttl_seconds": ttl_seconds if ttl_seconds is not None else 30,
        "timeout": timeout if timeout is not None else 3.0,
        "inbound_number": inbound_number or "",
        "return_dba": int(return_dba) if return_dba is not None else 0,
        "add_to_caps_on_status_reserved": int(add_to_caps_on_status_reserved) if add_to_caps_on_status_reserved is not None else 0,
        "route_only_to_reserved_target": int(route_only_to_reserved_target) if route_only_to_reserved_target is not None else 0,
        "allow_no_caller_number": int(allow_no_caller_number) if allow_no_caller_number is not None else 0,
        "paused": int(paused) if paused is not None else 0,
        "claim_percent_threshold": claim_percent_threshold if claim_percent_threshold is not None else 10,
        "blocked_inbound_percent": blocked_inbound_percent if blocked_inbound_percent is not None else 50,
        "ping_shield_outbound_count_limit": ping_shield_outbound_count_limit or "",
        "ping_shield_outbound_ms_limit": ping_shield_outbound_ms_limit or "",
    }
    return await client.post(
        f"/campaigns/{campaign_id}/postback_keys", {"postback_key": body}
    )


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_webhook(
    campaign_id: int,
    trigger_type: int,
    url: str,
    name: str | None = None,
    request_method: str | None = None,
    dedupe_seconds: int | None = None,
    tag_list: str | None = None,
) -> dict:
    """Create a basic webhook (timer) on a campaign. Do NOT use this for RTB —
    use create_rtb_webhook instead.

    Trigger types:
        9  = Call starts (fires when a call comes in)
        5  = Call converted
        13 = Data appending

    Parameters:
        campaign_id: Internal numeric campaign ID (not the user-set CID).
        trigger_type: When the webhook fires (9, 5, or 13). For RTB (12) use create_rtb_webhook.
        url: The webhook URL to call.
        name: Display name for this webhook.
        request_method: HTTP method — "get" or "post" (default "post").
        dedupe_seconds: Dedupe window in seconds (default 0).
        tag_list: Comma-separated tags to apply.
    """
    pixel: dict = {
        "_destroy": False,
        "id": "",
        "fire_order": 0,
        "request_method": request_method or "post",
        "url": url,
        "wcf_template_id": "",
        "wcf_target_id": "",
    }

    timer: dict = {
        "id": "",
        "_destroy": False,
        "trigger_type": trigger_type,
        "name": name or "",
        "dedupe_seconds": dedupe_seconds if dedupe_seconds is not None else 0,
        "tag_list": tag_list or "",
        "pixels_attributes": {"0": pixel},
    }

    return await client.post(
        f"/campaigns/{campaign_id}/timers", {"start_timer": timer}
    )


@mcp.tool()
async def create_rtb_webhook(
    campaign_id: int,
    wcf_target_id: int,
    wcf_template_id: str,
    output_tag_prefix: str,
    ping_url: str,
    ping_method: str = "POST",
    ping_headers: str = '{"Content-Type":"application/json"}',
    ping_data: str = "",
    ping_output_map: str = "",
    name: str | None = None,
    post_condition_key: str | None = None,
    post_condition_operator: str | None = None,
    post_condition_value: str | None = None,
    post_url: str | None = None,
    post_method: str | None = None,
    post_headers: str | None = None,
    post_data: str | None = None,
    post_output_map: str | None = None,
    payout_output_tag: str | None = None,
    payout_modifier_multiplier: str | None = None,
    revenue_output_tag: str | None = None,
    revenue_modifier_multiplier: str | None = None,
    timer_offset_tag: str | None = None,
    timer_offset_modifier: str | None = None,
    update_buyer_tags: str | None = None,
) -> dict:
    """Create an RTB passthrough webhook using the webhook configurator. Always use
    this tool (not create_webhook) when setting up RTB integrations.

    This auto-builds the webhook configurator URL from the provided fields.

    Parameters:
        campaign_id: Internal numeric campaign ID (not the user-set CID).
        wcf_target_id: The target ID in this campaign for the RTB buyer.
        wcf_template_id: Webhook configurator template (e.g. "ringba_rtb_ping_post").
        output_tag_prefix: Prefix for output tags (e.g. "ringba_125879").
        ping_url: The RTB endpoint URL to ping (e.g. "https://rtb.ringba.com/v1/production/ID.json").
        ping_method: HTTP method for the ping (default "POST").
        ping_headers: JSON string of headers for the ping (default '{"Content-Type":"application/json"}').
        ping_data: JSON string of the ping request body with Retreaver tokens like [nanp_caller_number].
        ping_output_map: JSON string mapping RTB response fields to Retreaver fields.
        name: Display name for this webhook.
        post_condition_key: Tag key to evaluate for the post-call webhook condition.
        post_condition_operator: Operator for post condition (e.g. "is_greater_than").
        post_condition_value: Value to compare against for post condition.
        post_url: Post-call webhook URL.
        post_method: Post-call HTTP method.
        post_headers: Post-call headers as JSON string.
        post_data: Post-call request body as JSON string.
        post_output_map: Post-call output mapping as JSON string.
        payout_output_tag: Tag to read payout from.
        payout_modifier_multiplier: Payout multiplier.
        revenue_output_tag: Tag to read revenue from.
        revenue_modifier_multiplier: Revenue multiplier.
        timer_offset_tag: Tag for timer offset.
        timer_offset_modifier: Timer offset modifier.
        update_buyer_tags: Tags to update on the buyer.
    """
    from urllib.parse import quote, urlencode

    # Build the webhook configurator URL with all config encoded as query params
    wcf_params = {
        "call_key": "[call_key]",
        "call_uuid": "[call_uuid]",
        "output_tag_prefix": output_tag_prefix,
        "ping_url": ping_url,
        "ping_method": ping_method,
        "ping_headers": ping_headers,
        "ping_data": ping_data,
        "ping_output_map": ping_output_map,
    }
    wcf_url = "https://retreaver.com/webhook-configurator/v1/?" + urlencode(
        wcf_params, quote_via=quote
    )

    pixel: dict = {
        "_destroy": False,
        "id": "",
        "fire_order": 0,
        "request_method": "post",
        "url": wcf_url,
        "wcf_template_id": wcf_template_id,
        "wcf_target_id": wcf_target_id,
    }

    timer: dict = {
        "id": "",
        "_destroy": False,
        "trigger_type": 12,
        "name": name or "config",
        "dedupe_seconds": 0,
        "tag_list": "",
        "pixels_attributes": {"0": pixel},
    }

    payload: dict = {
        "passthrough_timer": timer,
        "wcf_output_tag_prefix_field": output_tag_prefix,
        "wcf_ping_url_field": ping_url,
        "wcf_ping_method_field": ping_method,
        "wcf_ping_headers_field": ping_headers,
        "wcf_ping_data_field": ping_data,
        "wcf_ping_output_map_field": ping_output_map,
        "wcf_post_condition_key_field": post_condition_key or "",
        "wcf_post_condition_operator_field": post_condition_operator or "is_greater_than",
        "wcf_post_condition_value_field": post_condition_value or "",
        "wcf_post_url_field": post_url or "",
        "wcf_post_method_field": post_method or "POST",
        "wcf_post_headers_field": post_headers or "",
        "wcf_post_data_field": post_data or "",
        "wcf_post_output_map_field": post_output_map or "",
        "wcf_payout_output_tag_field": payout_output_tag or "",
        "wcf_payout_modifier_multiplier_field": payout_modifier_multiplier or "",
        "wcf_revenue_output_tag_field": revenue_output_tag or "",
        "wcf_revenue_modifier_multiplier_field": revenue_modifier_multiplier or "",
        "wcf_timer_offset_tag_field": timer_offset_tag or "",
        "wcf_timer_offset_modifier_field": timer_offset_modifier or "",
        "update_buyer_tags": update_buyer_tags or "",
    }

    return await client.post(f"/campaigns/{campaign_id}/timers", payload)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    from .process import handle_command, remove_pid, write_pid

    _NAME = "retreaver-write"

    if handle_command(_NAME):
        return

    import argparse
    import atexit

    parser = argparse.ArgumentParser(description="Retreaver write MCP server")
    parser.add_argument("command", nargs="?", default="start", choices=["start"], help="Command (default: start)")
    parser.add_argument("--port", type=int, default=8002, help="Port for SSE transport (default: 8002)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    args = parser.parse_args()

    write_pid(_NAME)
    atexit.register(remove_pid, _NAME)

    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
