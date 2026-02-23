"""MCP server exposing read-only (GET) tools for the Retreaver API."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .client import RetreaverClient

mcp = FastMCP("retreaver-read")
client = RetreaverClient()

# ---------------------------------------------------------------------------
# Calls
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_calls(
    page: int = 1,
    per_page: int = 25,
    created_at_start: str | None = None,
    created_at_end: str | None = None,
    sort_by: str | None = None,
    order: str | None = None,
    caller: str | None = None,
    client_afid: str | None = None,
    client_cid: str | None = None,
    client_tid: str | None = None,
    sub_id: str | None = None,
    call_flow_events: bool | None = None,
) -> dict | list:
    """List calls with optional filters. Uses the V3 calls endpoint.

    Parameters:
        page: Page number (default 1)
        per_page: Results per page (default 25)
        created_at_start: ISO-8601 start date filter (YYYY-MM-DDTHH:MM:SS+HH:MM)
        created_at_end: ISO-8601 end date filter (YYYY-MM-DDTHH:MM:SS+HH:MM)
        sort_by: 'created_at' or 'updated_at'
        order: 'asc' or 'desc'
        caller: Filter by caller phone number
        client_afid: Filter by affiliate ID
        client_cid: Filter by campaign ID
        client_tid: Filter by target ID
        sub_id: Filter by sub ID
        call_flow_events: If true, returns call flow events showing what happened during the call
    """
    params: dict = {"page": page, "per_page": per_page}
    for key, val in {
        "created_at_start": created_at_start,
        "created_at_end": created_at_end,
        "sort_by": sort_by,
        "order": order,
        "caller": caller,
        "client_afid": client_afid,
        "client_cid": client_cid,
        "client_tid": client_tid,
        "sub_id": sub_id,
        "call_flow_events": call_flow_events,
    }.items():
        if val is not None:
            params[key] = val
    return await client.get("/api/v3/calls.json", params)


@mcp.tool()
async def get_call(uuid: str) -> dict:
    """Get a single call by its UUID."""
    return await client.get(f"/api/v3/calls/{uuid}.json")


@mcp.tool()
async def check_call_flow(
    caller: str | None = None,
    uuid: str | None = None,
) -> dict | list:
    """Check what happened during a SINGLE call by looking up its call flow events.

    Only look up ONE call at a time. If you need to check multiple calls, call this
    tool once per call.

    Provide either a caller phone number OR a single call UUID (not both).

    Parameters:
        caller: A single caller phone number to look up.
        uuid: A single call UUID to look up (e.g. "addcf985-017e-4962-be34-cf5d55e74afc").
    """
    if uuid:
        uuid = uuid.strip()
        if " " in uuid or "," in uuid:
            return {"error": "Only one UUID at a time. Call this tool once per call."}
        return await client.get(
            f"/api/v2/calls/{uuid}.json",
            {"call_flow_events": "true"},
        )
    if caller:
        caller = caller.strip()
        return await client.get(
            "/api/v2/calls.json",
            {"caller": caller, "call_flow_events": "true"},
        )
    return {"error": "Provide either a caller phone number or a call UUID."}


# ---------------------------------------------------------------------------
# Affiliates
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_affiliates(page: int = 1) -> dict | list:
    """List all affiliates (25 per page)."""
    return await client.get("/affiliates.json", {"page": page})


@mcp.tool()
async def get_affiliate(afid: str) -> dict:
    """Get a single affiliate by AFID."""
    return await client.get(f"/affiliates/afid/{afid}.json")


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_targets(page: int = 1) -> dict | list:
    """List all targets (25 per page)."""
    return await client.get("/targets.json", {"page": page})


@mcp.tool()
async def get_target(target_id: int) -> dict:
    """Get a single target by internal ID."""
    return await client.get(f"/targets/{target_id}.json")


@mcp.tool()
async def get_target_by_tid(tid: str) -> dict:
    """Get a single target by customer-editable TID."""
    return await client.get(f"/targets/tid/{tid}.json")


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_campaigns(page: int = 1) -> dict | list:
    """List all campaigns (25 per page)."""
    return await client.get("/campaigns.json", {"page": page})


@mcp.tool()
async def get_campaign(cid: str) -> dict:
    """Get a single campaign by CID."""
    return await client.get(f"/campaigns/cid/{cid}.json")


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_numbers(page: int = 1) -> dict | list:
    """List all numbers (25 per page)."""
    return await client.get("/numbers.json", {"page": page})


@mcp.tool()
async def get_number(number_id: int) -> dict:
    """Get a single number by ID."""
    return await client.get(f"/numbers/{number_id}.json")


# ---------------------------------------------------------------------------
# Number Pools
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_number_pools(page: int = 1) -> dict | list:
    """List all number pools (25 per page)."""
    return await client.get("/number_pools.json", {"page": page})


@mcp.tool()
async def get_number_pool(pool_id: int) -> dict:
    """Get a single number pool by ID."""
    return await client.get(f"/number_pools/{pool_id}.json")


# ---------------------------------------------------------------------------
# Companies
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_active_company() -> dict:
    """Get the currently active company."""
    return await client.get("/company.json")


@mcp.tool()
async def get_companies(page: int = 1) -> dict | list:
    """List all companies (25 per page)."""
    return await client.get("/companies.json", {"page": page})


@mcp.tool()
async def get_company(company_id: int) -> dict:
    """Get a single company by ID."""
    return await client.get(f"/companies/{company_id}.json")


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_contacts(page: int = 1) -> dict | list:
    """List all contacts (25 per page)."""
    return await client.get("/contacts.json", {"page": page})


@mcp.tool()
async def get_contact(contact_id: int) -> dict:
    """Get a single contact by ID."""
    return await client.get(f"/contacts/{contact_id}.json")


@mcp.tool()
async def get_contact_by_phone(phone: str) -> dict:
    """Get a contact by phone number (E.164 format, e.g. +15551234567)."""
    return await client.get(f"/contacts/phone/{phone}.json")


# ---------------------------------------------------------------------------
# Caller Lists
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_caller_list(target_id: int, caller_list_name: str) -> dict:
    """Get a single caller list by name.

    Parameters:
        target_id: Target ID the caller list belongs to
        caller_list_name: Name of the caller list
    """
    return await client.get(f"/api/v2/targets/{target_id}/caller_lists/{caller_list_name}.json")


@mcp.tool()
async def get_caller_list_numbers(target_id: int, caller_list_name: str, page: int = 1) -> dict | list:
    """List phone numbers in a caller list (25 per page).

    Parameters:
        target_id: Target ID the caller list belongs to
        caller_list_name: Name of the caller list
        page: Page number
    """
    return await client.get(
        f"/api/v2/targets/{target_id}/caller_lists/{caller_list_name}/caller_list_numbers.json",
        {"page": page},
    )


# ---------------------------------------------------------------------------
# Suppressed Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_suppressed_numbers(page: int = 1) -> dict | list:
    """List all suppressed numbers (25 per page)."""
    return await client.get("/suppressed_numbers.json", {"page": page})


@mcp.tool()
async def get_suppressed_number(suppressed_number_id: int) -> dict:
    """Get a single suppressed number by ID."""
    return await client.get(f"/suppressed_numbers/{suppressed_number_id}.json")


# ---------------------------------------------------------------------------
# Static Caller Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_static_caller_numbers(page: int = 1) -> dict | list:
    """List all static caller numbers (25 per page)."""
    return await client.get("/static_caller_numbers.json", {"page": page})


# ---------------------------------------------------------------------------
# Target Groups
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_target_groups(page: int = 1) -> dict | list:
    """List all target groups (25 per page)."""
    return await client.get("/target_groups.json", {"page": page})


@mcp.tool()
async def get_target_group(target_group_id: int) -> dict:
    """Get a single target group by ID."""
    return await client.get(f"/target_groups/{target_group_id}.json")


# ---------------------------------------------------------------------------
# Search helpers
# ---------------------------------------------------------------------------


async def _fetch_all_pages(
    path: str,
    resource_key: str | None = None,
    extra_params: dict | None = None,
) -> list:
    """Fetch every page for a paginated endpoint, returning all records.

    Args:
        path: API endpoint path (e.g. "/targets.json").
        resource_key: If the API wraps each item in a key (e.g. "target"),
            unwrap it so callers get flat dicts with fields like "name".
        extra_params: Additional query parameters to include on every request.
    """
    all_items: list = []
    page = 1
    while True:
        params: dict = {"page": page, **(extra_params or {})}
        result = await client.get(path, params)
        if isinstance(result, dict) and "data" in result:
            items = result["data"]
            if resource_key:
                items = [item[resource_key] for item in items if resource_key in item]
            all_items.extend(items)
            if "next" not in result.get("pagination", {}):
                break
            page = result["pagination"]["next"]
        elif isinstance(result, list):
            items = result
            if resource_key:
                items = [item[resource_key] for item in items if resource_key in item]
            all_items.extend(items)
            break  # no pagination info means single page
        else:
            break
    return all_items


@mcp.tool()
async def search_targets(name: str) -> list:
    """Search all targets by name. Use this instead of paging through get_targets manually.

    Parameters:
        name: Case-insensitive substring to match against the target name.
    """
    all_targets = await _fetch_all_pages("/targets.json", "target")
    needle = name.lower()
    return [t for t in all_targets if needle in (t.get("name") or "").lower()]


@mcp.tool()
async def search_campaigns(name: str) -> list:
    """Search all campaigns by name. Use this instead of paging through get_campaigns manually.

    Parameters:
        name: Case-insensitive substring to match against the campaign name.
    """
    all_campaigns = await _fetch_all_pages("/campaigns.json", "campaign")
    needle = name.lower()
    return [c for c in all_campaigns if needle in (c.get("name") or "").lower()]


@mcp.tool()
async def search_affiliates(search: str) -> list:
    """Search all affiliates by name. Use this instead of paging through get_affiliates manually.

    Matches against company_name or first_name (case-insensitive).

    Parameters:
        search: Case-insensitive substring to match against company_name or first_name.
    """
    all_affiliates = await _fetch_all_pages("/affiliates.json", "affiliate")
    needle = search.lower()
    return [
        a for a in all_affiliates
        if needle in (a.get("company_name") or "").lower()
        or needle in (a.get("first_name") or "").lower()
    ]


@mcp.tool()
async def get_all_numbers() -> dict:
    """Fetch ALL numbers across every page and return them with a total count.

    Use this instead of paging through get_numbers manually. Returns
    {"total": <int>, "numbers": [...]}.
    """
    numbers = await _fetch_all_pages("/numbers.json", "number")
    return {"total": len(numbers), "numbers": numbers}


@mcp.tool()
async def get_all_targets() -> dict:
    """Fetch ALL targets across every page and return them with a total count.

    Use this instead of paging through get_targets manually. Returns
    {"total": <int>, "targets": [...]}.
    """
    targets = await _fetch_all_pages("/targets.json", "target")
    return {"total": len(targets), "targets": targets}


@mcp.tool()
async def get_all_campaigns() -> dict:
    """Fetch ALL campaigns across every page and return them with a total count.

    Use this instead of paging through get_campaigns manually. Returns
    {"total": <int>, "campaigns": [...]}.
    """
    campaigns = await _fetch_all_pages("/campaigns.json", "campaign")
    return {"total": len(campaigns), "campaigns": campaigns}


@mcp.tool()
async def get_all_affiliates() -> dict:
    """Fetch ALL affiliates/publishers across every page and return them with a total count.

    Use this instead of paging through get_affiliates manually. Returns
    {"total": <int>, "affiliates": [...]}.
    """
    affiliates = await _fetch_all_pages("/affiliates.json", "affiliate")
    return {"total": len(affiliates), "affiliates": affiliates}


@mcp.tool()
async def get_all_calls(
    created_at_start: str | None = None,
    created_at_end: str | None = None,
) -> dict:
    """Fetch ALL calls across every page and return them with a total count.

    Warning: this can be very large without date filters. Always pass a date range
    when possible.

    Parameters:
        created_at_start: ISO-8601 start date filter (YYYY-MM-DDTHH:MM:SS+HH:MM).
        created_at_end: ISO-8601 end date filter (YYYY-MM-DDTHH:MM:SS+HH:MM).
    """
    extra: dict = {"per_page": 100}
    if created_at_start is not None:
        extra["created_at_start"] = created_at_start
    if created_at_end is not None:
        extra["created_at_end"] = created_at_end
    calls = await _fetch_all_pages("/api/v3/calls.json", extra_params=extra)
    return {"total": len(calls), "calls": calls}


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_report_tag_value(
    tag_name: str,
    tag_value: str,
    created_at_start: str | None = None,
    created_at_end: str | None = None,
) -> dict:
    """Get report data for a specific tag value.

    Parameters:
        tag_name: The tag key name
        tag_value: The tag value to report on
        created_at_start: ISO-8601 start date
        created_at_end: ISO-8601 end date
    """
    params: dict = {"tag_name": tag_name, "tag_value": tag_value}
    if created_at_start is not None:
        params["created_at_start"] = created_at_start
    if created_at_end is not None:
        params["created_at_end"] = created_at_end
    return await client.get("/reports/tag_value.json", params)


@mcp.tool()
async def get_report_tag_value_name(
    tag_name: str,
    created_at_start: str | None = None,
    created_at_end: str | None = None,
) -> dict:
    """Get report data grouped by values for a given tag name.

    Parameters:
        tag_name: The tag key name to report on
        created_at_start: ISO-8601 start date
        created_at_end: ISO-8601 end date
    """
    params: dict = {"tag_name": tag_name}
    if created_at_start is not None:
        params["created_at_start"] = created_at_start
    if created_at_end is not None:
        params["created_at_end"] = created_at_end
    return await client.get("/reports/tag_value_name.json", params)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    from .process import handle_command, remove_pid, write_pid

    _NAME = "retreaver-read"

    if handle_command(_NAME):
        return

    import argparse
    import atexit

    parser = argparse.ArgumentParser(description="Retreaver read-only MCP server")
    parser.add_argument("command", nargs="?", default="start", choices=["start"], help="Command (default: start)")
    parser.add_argument("--port", type=int, default=8001, help="Port for SSE transport (default: 8001)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    args = parser.parse_args()

    write_pid(_NAME)
    atexit.register(remove_pid, _NAME)

    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
