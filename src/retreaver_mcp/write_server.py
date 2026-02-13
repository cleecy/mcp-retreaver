"""MCP server exposing write (POST/PUT/DELETE) tools for the Retreaver API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .client import RetreaverClient

mcp = FastMCP("retreaver-write")
client = RetreaverClient()

# ---------------------------------------------------------------------------
# Affiliates
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_affiliate(
    afid: str,
    first_name: str | None = None,
    last_name: str | None = None,
    company_name: str | None = None,
) -> dict:
    """Create a new affiliate.

    Parameters:
        afid: Unique affiliate ID
        first_name: First name
        last_name: Last name
        company_name: Company name
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
async def update_affiliate(
    afid: str,
    first_name: str | None = None,
    last_name: str | None = None,
    company_name: str | None = None,
) -> dict:
    """Update an existing affiliate by AFID.

    Parameters:
        afid: Affiliate ID to update
        first_name: New first name
        last_name: New last name
        company_name: New company name
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
async def delete_affiliate(afid: str) -> dict | str:
    """Delete an affiliate by AFID."""
    return await client.delete(f"/affiliates/afid/{afid}.json")


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
) -> dict:
    """Create a new target (call destination).

    Parameters:
        number: Phone number in E.164 format (e.g. +18668987878)
        name: Display name for the target
        tid: Custom target ID
        priority: Routing priority (lower = higher priority)
        weight: Routing weight for load balancing
        timeout_seconds: Ring timeout in seconds
        inband_signals: Enable in-band signal detection
        timer_offset: Timer offset in seconds
        send_digits: DTMF digits to send after connection (e.g. "1w2")
        concurrency_cap: Max simultaneous calls
        paused: Whether the target is paused
        time_zone: Time zone (e.g. "UTC", "America/New_York")
        sip_username: SIP username
        sip_password: SIP password
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
    return await client.post("/targets.json", {"target": body})


@mcp.tool()
async def update_target(
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
) -> dict:
    """Update an existing target by ID.

    Parameters:
        target_id: Target ID to update
        number: Phone number in E.164 format
        name: Display name
        tid: Custom target ID
        priority: Routing priority
        weight: Routing weight
        timeout_seconds: Ring timeout in seconds
        inband_signals: Enable in-band signal detection
        timer_offset: Timer offset in seconds
        send_digits: DTMF digits to send
        concurrency_cap: Max simultaneous calls
        paused: Whether the target is paused
        time_zone: Time zone
        sip_username: SIP username
        sip_password: SIP password
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
    return await client.put(f"/targets/{target_id}.json", {"target": body})


@mcp.tool()
async def delete_target(target_id: int) -> dict | str:
    """Delete a target by ID."""
    return await client.delete(f"/targets/{target_id}.json")


@mcp.tool()
async def update_target_tags(target_id: int, tag_list: str) -> dict:
    """Update tags on a target.

    Parameters:
        target_id: Target ID
        tag_list: Comma-separated tags in Retreaver format, e.g.
                  "<<<calling_about:support>>>,<<<calling_about:other>>>"
    """
    return await client.put(
        f"/targets/{target_id}.json",
        {"target": {"tag_list": tag_list}},
    )


@mcp.tool()
async def update_target_caps(
    target_id: int,
    hard_cap: int | None = None,
    hourly_cap: int | None = None,
    daily_cap: int | None = None,
    monthly_cap: int | None = None,
) -> dict:
    """Update call caps on a target.

    Parameters:
        target_id: Target ID
        hard_cap: Concurrency / hard cap
        hourly_cap: Max calls per hour
        daily_cap: Max calls per day
        monthly_cap: Max calls per month
    """
    body: dict = {}
    if hard_cap is not None:
        body["hard_cap_attributes"] = {"cap": hard_cap}
    if hourly_cap is not None:
        body["hourly_cap_attributes"] = {"cap": hourly_cap}
    if daily_cap is not None:
        body["daily_cap_attributes"] = {"cap": daily_cap}
    if monthly_cap is not None:
        body["monthly_cap_attributes"] = {"cap": monthly_cap}
    return await client.put(f"/targets/{target_id}.json", {"target": body})


@mcp.tool()
async def reset_target_cap(target_id: int) -> dict:
    """Reset the call cap counters for a target."""
    return await client.post(f"/targets/{target_id}/reset_cap.json")


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
    timers: list[dict] | None = None,
    menu_options: list[dict] | None = None,
) -> dict:
    """Create a new campaign.

    Parameters:
        cid: Unique campaign ID
        name: Campaign name
        dedupe_seconds: Deduplicate calls within this many seconds
        affiliate_can_pull_number: Allow affiliates to pull tracking numbers
        record_calls: Record calls
        message: IVR greeting message text
        voice_gender: "Male" or "Female" for TTS
        repeat: Number of times to repeat the message
        timers: List of timer dicts, e.g. [{"seconds": 0, "url": "..."}]
        menu_options: List of menu option dicts, e.g. [{"option": "1", "target_number": "+1..."}]
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
    if timers is not None:
        body["timers_attributes"] = timers
    if menu_options is not None:
        body["menu_options_attributes"] = menu_options
    return await client.post("/campaigns.json", {"campaign": body})


@mcp.tool()
async def update_campaign(
    cid: str,
    name: str | None = None,
    dedupe_seconds: int | None = None,
    affiliate_can_pull_number: bool | None = None,
    record_calls: bool | None = None,
    message: str | None = None,
    voice_gender: str | None = None,
    repeat: int | None = None,
    timers: list[dict] | None = None,
    menu_options: list[dict] | None = None,
    destroy_nested: bool | None = None,
) -> dict:
    """Update an existing campaign by CID.

    Parameters:
        cid: Campaign ID to update
        name: Campaign name
        dedupe_seconds: Deduplicate calls within this many seconds
        affiliate_can_pull_number: Allow affiliates to pull tracking numbers
        record_calls: Record calls
        message: IVR greeting message text
        voice_gender: "Male" or "Female"
        repeat: Repeat count
        timers: List of timer dicts
        menu_options: List of menu option dicts
        destroy_nested: If true, remove nested timers/menu options not in the update
    """
    body: dict = {}
    for key, val in {
        "name": name, "dedupe_seconds": dedupe_seconds,
        "affiliate_can_pull_number": affiliate_can_pull_number,
        "record_calls": record_calls, "message": message,
        "voice_gender": voice_gender, "repeat": repeat,
        "destroy_nested": destroy_nested,
    }.items():
        if val is not None:
            body[key] = val
    if timers is not None:
        body["timers_attributes"] = timers
    if menu_options is not None:
        body["menu_options_attributes"] = menu_options
    return await client.put(f"/campaigns/cid/{cid}.json", {"campaign": body})


@mcp.tool()
async def delete_campaign(cid: str) -> dict | str:
    """Delete a campaign by CID."""
    return await client.delete(f"/campaigns/cid/{cid}.json")


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_number(
    cid: str,
    number_type: str = "Toll-free",
    country: str = "US",
    afid: str | None = None,
    sid: str | None = None,
    desired_text: str | None = None,
    message: str | None = None,
    voice_gender: str | None = None,
    repeat: int | None = None,
    timers: list[dict] | None = None,
    menu_options: list[dict] | None = None,
) -> dict:
    """Provision a new tracking number.

    Parameters:
        cid: Campaign ID to assign the number to
        number_type: "Toll-free" or "Local"
        country: Country code (e.g. "US", "CA")
        afid: Affiliate ID
        sid: Sub ID
        desired_text: Vanity text to search for (e.g. "TEST")
        message: IVR greeting text
        voice_gender: "Male" or "Female"
        repeat: Message repeat count
        timers: List of timer dicts
        menu_options: List of menu option dicts
    """
    body: dict = {"cid": cid, "type": number_type, "country": country}
    for key, val in {
        "afid": afid, "sid": sid, "desired_text": desired_text,
        "message": message, "voice_gender": voice_gender, "repeat": repeat,
    }.items():
        if val is not None:
            body[key] = val
    if timers is not None:
        body["timers_attributes"] = timers
    if menu_options is not None:
        body["menu_options_attributes"] = menu_options
    return await client.post("/numbers.json", {"number": body})


@mcp.tool()
async def update_number(
    number_id: int,
    afid: str | None = None,
    cid: str | None = None,
    sid: str | None = None,
    message: str | None = None,
    voice_gender: str | None = None,
    repeat: int | None = None,
    timers: list[dict] | None = None,
    menu_options: list[dict] | None = None,
    destroy_nested: bool | None = None,
) -> dict:
    """Update an existing number by ID.

    Parameters:
        number_id: Number ID to update
        afid: Affiliate ID
        cid: Campaign ID
        sid: Sub ID
        message: IVR greeting text
        voice_gender: "Male" or "Female"
        repeat: Message repeat count
        timers: List of timer dicts
        menu_options: List of menu option dicts
        destroy_nested: If true, remove nested attrs not in the update
    """
    body: dict = {}
    for key, val in {
        "afid": afid, "cid": cid, "sid": sid,
        "message": message, "voice_gender": voice_gender,
        "repeat": repeat, "destroy_nested": destroy_nested,
    }.items():
        if val is not None:
            body[key] = val
    if timers is not None:
        body["timers_attributes"] = timers
    if menu_options is not None:
        body["menu_options_attributes"] = menu_options
    return await client.put(f"/numbers/{number_id}.json", {"number": body})


@mcp.tool()
async def delete_number(number_id: int) -> dict | str:
    """Delete (release) a number by ID."""
    return await client.delete(f"/numbers/{number_id}.json")


# ---------------------------------------------------------------------------
# Number Pools
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_number_pool(
    cid: str,
    number_type: str = "Toll-free",
    country: str = "US",
    afid: str | None = None,
    max_pool_size: int | None = None,
    buffer_seconds: int | None = None,
    hide_embedded_access: bool | None = None,
    google_analytics: bool | None = None,
    reserve_size: int | None = None,
) -> dict:
    """Create a new number pool for dynamic number insertion.

    Parameters:
        cid: Campaign ID
        number_type: "Toll-free" or "Local"
        country: Country code
        afid: Affiliate ID
        max_pool_size: Maximum numbers in the pool
        buffer_seconds: Seconds to buffer before recycling
        hide_embedded_access: Hide embedded JS access
        google_analytics: Enable GA integration
        reserve_size: Number of reserved numbers
    """
    body: dict = {"cid": cid, "type": number_type, "country": country}
    for key, val in {
        "afid": afid, "max_pool_size": max_pool_size,
        "buffer_seconds": buffer_seconds,
        "hide_embedded_access": hide_embedded_access,
        "google_analytics": google_analytics, "reserve_size": reserve_size,
    }.items():
        if val is not None:
            body[key] = val
    return await client.post("/number_pools.json", {"number_pool": body})


@mcp.tool()
async def update_number_pool(
    pool_id: int,
    max_pool_size: int | None = None,
    buffer_seconds: int | None = None,
    hide_embedded_access: bool | None = None,
    google_analytics: bool | None = None,
    reserve_size: int | None = None,
) -> dict:
    """Update an existing number pool by ID.

    Parameters:
        pool_id: Number pool ID
        max_pool_size: Maximum numbers in the pool
        buffer_seconds: Seconds to buffer before recycling
        hide_embedded_access: Hide embedded JS access
        google_analytics: Enable GA integration
        reserve_size: Number of reserved numbers
    """
    body: dict = {}
    for key, val in {
        "max_pool_size": max_pool_size, "buffer_seconds": buffer_seconds,
        "hide_embedded_access": hide_embedded_access,
        "google_analytics": google_analytics, "reserve_size": reserve_size,
    }.items():
        if val is not None:
            body[key] = val
    return await client.put(f"/number_pools/{pool_id}.json", {"number_pool": body})


@mcp.tool()
async def delete_number_pool(pool_id: int) -> dict | str:
    """Delete a number pool by ID."""
    return await client.delete(f"/number_pools/{pool_id}.json")


# ---------------------------------------------------------------------------
# Companies
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_company(name: str) -> dict:
    """Create a new company.

    Parameters:
        name: Company name
    """
    return await client.post("/companies.json", {"company": {"name": name}})


@mcp.tool()
async def update_company(
    company_id: int,
    name: str | None = None,
) -> dict:
    """Update an existing company by ID.

    Parameters:
        company_id: Company ID to update
        name: New company name
    """
    body: dict = {}
    if name is not None:
        body["name"] = name
    return await client.put(f"/companies/{company_id}.json", {"company": body})


@mcp.tool()
async def delete_company(company_id: int) -> dict | str:
    """Delete a company by ID."""
    return await client.delete(f"/companies/{company_id}.json")


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_contact(
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
) -> dict:
    """Create a new contact.

    Parameters:
        first_name: First name
        last_name: Last name
        phone: Phone number in E.164 format
        email: Email address
    """
    body: dict = {}
    for key, val in {
        "first_name": first_name, "last_name": last_name,
        "phone": phone, "email": email,
    }.items():
        if val is not None:
            body[key] = val
    return await client.post("/contacts.json", {"contact": body})


@mcp.tool()
async def update_contact(
    contact_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
) -> dict:
    """Update an existing contact by ID.

    Parameters:
        contact_id: Contact ID to update
        first_name: First name
        last_name: Last name
        phone: Phone number
        email: Email address
    """
    body: dict = {}
    for key, val in {
        "first_name": first_name, "last_name": last_name,
        "phone": phone, "email": email,
    }.items():
        if val is not None:
            body[key] = val
    return await client.put(f"/contacts/{contact_id}.json", {"contact": body})


@mcp.tool()
async def delete_contact(contact_id: int) -> dict | str:
    """Delete a contact by ID."""
    return await client.delete(f"/contacts/{contact_id}.json")


@mcp.tool()
async def update_contact_by_phone(
    phone: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> dict:
    """Update a contact by phone number.

    Parameters:
        phone: Phone number in E.164 format (e.g. +15551234567)
        first_name: First name
        last_name: Last name
        email: Email address
    """
    body: dict = {}
    for key, val in {
        "first_name": first_name, "last_name": last_name, "email": email,
    }.items():
        if val is not None:
            body[key] = val
    return await client.put(f"/contacts/phone/{phone}.json", {"contact": body})


@mcp.tool()
async def delete_contact_by_phone(phone: str) -> dict | str:
    """Delete a contact by phone number (E.164 format)."""
    return await client.delete(f"/contacts/phone/{phone}.json")


# ---------------------------------------------------------------------------
# Contact Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def update_contact_number_by_phone(
    phone: str,
    fields: dict | None = None,
) -> dict:
    """Update a contact number record by phone number.

    Parameters:
        phone: Phone number in E.164 format
        fields: Dict of contact number fields to update
    """
    return await client.put(
        f"/contact_numbers/phone/{phone}.json",
        {"contact_number": fields or {}},
    )


@mcp.tool()
async def delete_contact_number_by_phone(phone: str) -> dict | str:
    """Delete a contact number record by phone number."""
    return await client.delete(f"/contact_numbers/phone/{phone}.json")


# ---------------------------------------------------------------------------
# Caller Lists
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_caller_list(name: str) -> dict:
    """Create a new caller list.

    Parameters:
        name: Name of the caller list
    """
    return await client.post("/caller_lists.json", {"caller_list": {"name": name}})


@mcp.tool()
async def update_caller_list(caller_list_id: int, name: str) -> dict:
    """Update a caller list by ID.

    Parameters:
        caller_list_id: Caller list ID
        name: New name for the caller list
    """
    return await client.put(
        f"/caller_lists/{caller_list_id}.json",
        {"caller_list": {"name": name}},
    )


@mcp.tool()
async def delete_caller_list(caller_list_id: int) -> dict | str:
    """Delete a caller list by ID."""
    return await client.delete(f"/caller_lists/{caller_list_id}.json")


@mcp.tool()
async def add_caller_list_number(caller_list_id: int, number: str) -> dict:
    """Add a phone number to a caller list.

    Parameters:
        caller_list_id: Caller list ID
        number: Phone number to add (E.164 format)
    """
    return await client.post(
        f"/caller_lists/{caller_list_id}/numbers.json",
        {"number": number},
    )


# ---------------------------------------------------------------------------
# Suppressed Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_suppressed_number(number: str) -> dict:
    """Create a new suppressed number.

    Parameters:
        number: Phone number to suppress (E.164 format, e.g. +15551234567)
    """
    return await client.post(
        "/suppressed_numbers.json",
        {"suppressed_number": {"number": number}},
    )


@mcp.tool()
async def update_suppressed_number(suppressed_number_id: int, number: str) -> dict:
    """Update a suppressed number by ID.

    Parameters:
        suppressed_number_id: Suppressed number ID
        number: New phone number
    """
    return await client.put(
        f"/suppressed_numbers/{suppressed_number_id}.json",
        {"suppressed_number": {"number": number}},
    )


@mcp.tool()
async def delete_suppressed_number(suppressed_number_id: int) -> dict | str:
    """Delete a suppressed number by ID."""
    return await client.delete(f"/suppressed_numbers/{suppressed_number_id}.json")


# ---------------------------------------------------------------------------
# Static Caller Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_static_caller_number(
    number: str,
    cid: str | None = None,
    afid: str | None = None,
) -> dict:
    """Create a static caller number mapping.

    Parameters:
        number: Phone number (E.164 format)
        cid: Campaign ID
        afid: Affiliate ID
    """
    body: dict = {"number": number}
    if cid is not None:
        body["cid"] = cid
    if afid is not None:
        body["afid"] = afid
    return await client.post("/static_caller_numbers.json", {"static_caller_number": body})


@mcp.tool()
async def delete_static_caller_number(static_caller_number_id: int) -> dict | str:
    """Delete a static caller number by ID."""
    return await client.delete(f"/static_caller_numbers/{static_caller_number_id}.json")


# ---------------------------------------------------------------------------
# Target Groups
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_target_group(
    name: str,
    priority: int | None = None,
    weight: int | None = None,
) -> dict:
    """Create a new target group.

    Parameters:
        name: Group name
        priority: Routing priority
        weight: Routing weight
    """
    body: dict = {"name": name}
    if priority is not None:
        body["priority"] = priority
    if weight is not None:
        body["weight"] = weight
    return await client.post("/target_groups.json", {"target_group": body})


@mcp.tool()
async def update_target_group(
    target_group_id: int,
    name: str | None = None,
    priority: int | None = None,
    weight: int | None = None,
) -> dict:
    """Update a target group by ID.

    Parameters:
        target_group_id: Target group ID
        name: Group name
        priority: Routing priority
        weight: Routing weight
    """
    body: dict = {}
    for key, val in {
        "name": name, "priority": priority, "weight": weight,
    }.items():
        if val is not None:
            body[key] = val
    return await client.put(f"/target_groups/{target_group_id}.json", {"target_group": body})


@mcp.tool()
async def delete_target_group(target_group_id: int) -> dict | str:
    """Delete a target group by ID."""
    return await client.delete(f"/target_groups/{target_group_id}.json")


@mcp.tool()
async def set_target_group_targets(target_group_id: int, target_ids: list[int]) -> dict:
    """Replace all targets in a group with the specified list.

    Parameters:
        target_group_id: Target group ID
        target_ids: List of target IDs to set as the group's targets
    """
    return await client.put(
        f"/target_groups/{target_group_id}/targets.json",
        {"target_ids": target_ids},
    )


@mcp.tool()
async def add_targets_to_group(target_group_id: int, target_ids: list[int]) -> dict:
    """Add targets to a target group.

    Parameters:
        target_group_id: Target group ID
        target_ids: List of target IDs to add
    """
    return await client.post(
        f"/target_groups/{target_group_id}/add_targets.json",
        {"target_ids": target_ids},
    )


@mcp.tool()
async def remove_targets_from_group(target_group_id: int, target_ids: list[int]) -> dict:
    """Remove targets from a target group.

    Parameters:
        target_group_id: Target group ID
        target_ids: List of target IDs to remove
    """
    return await client.post(
        f"/target_groups/{target_group_id}/remove_targets.json",
        {"target_ids": target_ids},
    )


@mcp.tool()
async def update_target_group_caps(
    target_group_id: int,
    hard_cap: int | None = None,
    hourly_cap: int | None = None,
    daily_cap: int | None = None,
    monthly_cap: int | None = None,
) -> dict:
    """Update call caps on a target group.

    Parameters:
        target_group_id: Target group ID
        hard_cap: Concurrency / hard cap
        hourly_cap: Max calls per hour
        daily_cap: Max calls per day
        monthly_cap: Max calls per month
    """
    body: dict = {}
    if hard_cap is not None:
        body["hard_cap_attributes"] = {"cap": hard_cap}
    if hourly_cap is not None:
        body["hourly_cap_attributes"] = {"cap": hourly_cap}
    if daily_cap is not None:
        body["daily_cap_attributes"] = {"cap": daily_cap}
    if monthly_cap is not None:
        body["monthly_cap_attributes"] = {"cap": monthly_cap}
    return await client.put(f"/target_groups/{target_group_id}.json", {"target_group": body})


@mcp.tool()
async def reset_target_group_caps(target_group_id: int) -> dict:
    """Reset all cap counters for a target group."""
    return await client.post(f"/target_groups/{target_group_id}/reset_caps.json")


# ---------------------------------------------------------------------------
# Call Data Writing (retreaverdata.com)
# ---------------------------------------------------------------------------


@mcp.tool()
async def write_call_data(
    key: str,
    caller_number: str | None = None,
    call_uuid: str | None = None,
    tags: dict | None = None,
) -> dict:
    """Write call data to Retreaver (posts to retreaverdata.com).

    Parameters:
        key: Postback key UUID
        caller_number: Caller phone number (E.164)
        call_uuid: Call UUID to associate data with
        tags: Dict of arbitrary key-value data tags (e.g. {"age": "39", "utm_campaign": "auto"})
    """
    body: dict = {"key": key, **(tags or {})}
    if caller_number is not None:
        body["caller_number"] = caller_number
    if call_uuid is not None:
        body["call_uuid"] = call_uuid
    return await client.post("https://retreaverdata.com/data_writing", body)


# ---------------------------------------------------------------------------
# RTB (Real-Time Bidding)
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_rtb_reservation(
    caller: str,
    cid: str | None = None,
    afid: str | None = None,
    tags: dict | None = None,
) -> dict:
    """Create an RTB reservation for a caller.

    Parameters:
        caller: Caller phone number (E.164)
        cid: Campaign ID
        afid: Affiliate ID
        tags: Additional reservation parameters / tags as key-value pairs
    """
    body: dict = {"caller": caller, **(tags or {})}
    if cid is not None:
        body["cid"] = cid
    if afid is not None:
        body["afid"] = afid
    return await client.post("/rtb/reservations.json", body)


@mcp.tool()
async def confirm_rtb_reservation(reservation_id: int) -> dict:
    """Confirm an RTB reservation.

    Parameters:
        reservation_id: Reservation ID returned from create_rtb_reservation
    """
    return await client.post(f"/rtb/reservations/{reservation_id}/confirm.json")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Retreaver write MCP server")
    parser.add_argument("--port", type=int, default=8002, help="Port for SSE transport (default: 8002)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    args = parser.parse_args()

    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
