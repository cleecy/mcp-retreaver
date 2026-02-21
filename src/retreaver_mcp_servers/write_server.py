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
    body: dict = {"action": "rtb"}
    for key, val in {
        "name": name, "tag_prefix": tag_prefix, "ttl_seconds": ttl_seconds,
        "timeout": timeout, "inbound_number": inbound_number,
        "claim_percent_threshold": claim_percent_threshold,
        "blocked_inbound_percent": blocked_inbound_percent,
        "ping_shield_outbound_count_limit": ping_shield_outbound_count_limit,
        "ping_shield_outbound_ms_limit": ping_shield_outbound_ms_limit,
    }.items():
        if val is not None:
            body[key] = val
    # Boolean/int flags sent as 0/1
    for key, val in {
        "return_dba": return_dba,
        "add_to_caps_on_status_reserved": add_to_caps_on_status_reserved,
        "route_only_to_reserved_target": route_only_to_reserved_target,
        "allow_no_caller_number": allow_no_caller_number,
        "paused": paused,
    }.items():
        if val is not None:
            body[key] = int(val)
    return await client.post(
        f"/campaigns/{campaign_id}/postback_keys.json", {"postback_key": body}
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
    wcf_template_id: str | None = None,
    wcf_target_id: int | None = None,
    wcf_output_tag_prefix_field: str | None = None,
    wcf_ping_url_field: str | None = None,
    wcf_ping_method_field: str | None = None,
    wcf_ping_headers_field: str | None = None,
    wcf_ping_data_field: str | None = None,
    wcf_ping_output_map_field: str | None = None,
    wcf_post_condition_key_field: str | None = None,
    wcf_post_condition_operator_field: str | None = None,
    wcf_post_condition_value_field: str | None = None,
    wcf_post_url_field: str | None = None,
    wcf_post_method_field: str | None = None,
    wcf_post_headers_field: str | None = None,
    wcf_post_data_field: str | None = None,
    wcf_post_output_map_field: str | None = None,
    wcf_payout_output_tag_field: str | None = None,
    wcf_payout_modifier_multiplier_field: str | None = None,
    wcf_revenue_output_tag_field: str | None = None,
    wcf_revenue_modifier_multiplier_field: str | None = None,
    wcf_timer_offset_tag_field: str | None = None,
    wcf_timer_offset_modifier_field: str | None = None,
    update_buyer_tags: str | None = None,
) -> dict:
    """Create a webhook (timer) on a campaign, with optional webhook configurator fields.

    Trigger types:
        9  = Call starts (fires when a call comes in)
        5  = Call converted
        12 = Passthrough / RTB (for brokering with RTB publishers and buyers)
        13 = Data appending

    Parameters:
        campaign_id: Internal numeric campaign ID (not the user-set CID).
        trigger_type: When the webhook fires (9, 5, 12, or 13).
        url: The webhook URL to call.
        name: Display name for this webhook.
        request_method: HTTP method — "get" or "post" (default "post").
        dedupe_seconds: Dedupe window in seconds (default 0).
        tag_list: Comma-separated tags to apply.
        wcf_template_id: Webhook configurator template ID (e.g. "ringba_rtb_ping_post").
        wcf_target_id: Target ID for the webhook configurator.
        wcf_output_tag_prefix_field: Tag prefix for webhook configurator output tags.
        wcf_ping_url_field: Ping URL for webhook configurator.
        wcf_ping_method_field: Ping HTTP method (default "POST").
        wcf_ping_headers_field: Ping headers as JSON string.
        wcf_ping_data_field: Ping request body as JSON string.
        wcf_ping_output_map_field: Ping output mapping as JSON string.
        wcf_post_condition_key_field: Post condition key for conditional post-call webhook.
        wcf_post_condition_operator_field: Post condition operator (e.g. "is_greater_than").
        wcf_post_condition_value_field: Post condition value.
        wcf_post_url_field: Post-call webhook URL.
        wcf_post_method_field: Post-call HTTP method (default "POST").
        wcf_post_headers_field: Post-call headers as JSON string.
        wcf_post_data_field: Post-call request body as JSON string.
        wcf_post_output_map_field: Post-call output mapping as JSON string.
        wcf_payout_output_tag_field: Tag to read payout from.
        wcf_payout_modifier_multiplier_field: Payout multiplier.
        wcf_revenue_output_tag_field: Tag to read revenue from.
        wcf_revenue_modifier_multiplier_field: Revenue multiplier.
        wcf_timer_offset_tag_field: Tag for timer offset.
        wcf_timer_offset_modifier_field: Timer offset modifier.
        update_buyer_tags: Tags to update on the buyer.
    """
    # Use "passthrough_timer" key for trigger_type 12, "start_timer" for others
    timer_key = "passthrough_timer" if trigger_type == 12 else "start_timer"

    pixel: dict = {
        "_destroy": False,
        "id": "",
        "fire_order": 0,
        "request_method": request_method or "post",
        "url": url,
    }
    if wcf_template_id is not None:
        pixel["wcf_template_id"] = wcf_template_id
    if wcf_target_id is not None:
        pixel["wcf_target_id"] = wcf_target_id

    timer: dict = {
        "id": "",
        "_destroy": False,
        "trigger_type": trigger_type,
        "name": name or "",
        "dedupe_seconds": dedupe_seconds or 0,
        "tag_list": tag_list or "",
        "pixels_attributes": {"0": pixel},
    }

    payload: dict = {timer_key: timer}

    # Webhook configurator fields (top-level in the request body)
    for key, val in {
        "wcf_output_tag_prefix_field": wcf_output_tag_prefix_field,
        "wcf_ping_url_field": wcf_ping_url_field,
        "wcf_ping_method_field": wcf_ping_method_field,
        "wcf_ping_headers_field": wcf_ping_headers_field,
        "wcf_ping_data_field": wcf_ping_data_field,
        "wcf_ping_output_map_field": wcf_ping_output_map_field,
        "wcf_post_condition_key_field": wcf_post_condition_key_field,
        "wcf_post_condition_operator_field": wcf_post_condition_operator_field,
        "wcf_post_condition_value_field": wcf_post_condition_value_field,
        "wcf_post_url_field": wcf_post_url_field,
        "wcf_post_method_field": wcf_post_method_field,
        "wcf_post_headers_field": wcf_post_headers_field,
        "wcf_post_data_field": wcf_post_data_field,
        "wcf_post_output_map_field": wcf_post_output_map_field,
        "wcf_payout_output_tag_field": wcf_payout_output_tag_field,
        "wcf_payout_modifier_multiplier_field": wcf_payout_modifier_multiplier_field,
        "wcf_revenue_output_tag_field": wcf_revenue_output_tag_field,
        "wcf_revenue_modifier_multiplier_field": wcf_revenue_modifier_multiplier_field,
        "wcf_timer_offset_tag_field": wcf_timer_offset_tag_field,
        "wcf_timer_offset_modifier_field": wcf_timer_offset_modifier_field,
        "update_buyer_tags": update_buyer_tags,
    }.items():
        if val is not None:
            payload[key] = val

    return await client.post(f"/campaigns/{campaign_id}/timers.json", payload)


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
