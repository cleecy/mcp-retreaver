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
) -> dict | list:
    """List calls with optional filters. Uses the V2 calls endpoint.

    Parameters:
        page: Page number (default 1)
        per_page: Results per page, max 100 (default 25)
        created_at_start: ISO-8601 start date filter
        created_at_end: ISO-8601 end date filter
        sort_by: Field to sort by
        order: 'asc' or 'desc'
        caller: Filter by caller phone number
        client_afid: Filter by affiliate ID
        client_cid: Filter by campaign ID
        client_tid: Filter by target ID
        sub_id: Filter by sub ID
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
    }.items():
        if val is not None:
            params[key] = val
    return await client.get("/api/v2/calls.json", params)


@mcp.tool()
async def get_call(uuid: str) -> dict:
    """Get a single call by its UUID."""
    return await client.get(f"/api/v2/calls/{uuid}.json")


# ---------------------------------------------------------------------------
# Affiliates
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_affiliates(page: int = 1, per_page: int = 25) -> dict | list:
    """List all affiliates."""
    return await client.get("/affiliates.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_affiliate(afid: str) -> dict:
    """Get a single affiliate by AFID."""
    return await client.get(f"/affiliates/afid/{afid}.json")


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_targets(page: int = 1, per_page: int = 25) -> dict | list:
    """List all targets."""
    return await client.get("/targets.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_target(target_id: int) -> dict:
    """Get a single target by ID."""
    return await client.get(f"/targets/{target_id}.json")


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_campaigns(page: int = 1, per_page: int = 25) -> dict | list:
    """List all campaigns."""
    return await client.get("/campaigns.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_campaign(cid: str) -> dict:
    """Get a single campaign by CID."""
    return await client.get(f"/campaigns/cid/{cid}.json")


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_numbers(
    page: int = 1,
    per_page: int = 25,
    client_cid: str | None = None,
    client_afid: str | None = None,
    sub_id: str | None = None,
) -> dict | list:
    """List numbers with optional filters.

    Parameters:
        page: Page number
        per_page: Results per page, max 100
        client_cid: Filter by campaign ID
        client_afid: Filter by affiliate ID
        sub_id: Filter by sub ID
    """
    params: dict = {"page": page, "per_page": per_page}
    if client_cid is not None:
        params["client_cid"] = client_cid
    if client_afid is not None:
        params["client_afid"] = client_afid
    if sub_id is not None:
        params["sub_id"] = sub_id
    return await client.get("/numbers.json", params)


@mcp.tool()
async def get_number(number_id: int) -> dict:
    """Get a single number by ID."""
    return await client.get(f"/numbers/{number_id}.json")


# ---------------------------------------------------------------------------
# Number Pools
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_number_pools(
    page: int = 1,
    per_page: int = 25,
    cid: str | None = None,
    afid: str | None = None,
) -> dict | list:
    """List number pools with optional filters.

    Parameters:
        page: Page number
        per_page: Results per page, max 100
        cid: Filter by campaign ID
        afid: Filter by affiliate ID
    """
    params: dict = {"page": page, "per_page": per_page}
    if cid is not None:
        params["cid"] = cid
    if afid is not None:
        params["afid"] = afid
    return await client.get("/number_pools.json", params)


@mcp.tool()
async def get_number_pool(pool_id: int) -> dict:
    """Get a single number pool by ID."""
    return await client.get(f"/number_pools/{pool_id}.json")


# ---------------------------------------------------------------------------
# Companies
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_companies(page: int = 1, per_page: int = 25) -> dict | list:
    """List all companies."""
    return await client.get("/companies.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_company(company_id: int) -> dict:
    """Get a single company by ID."""
    return await client.get(f"/companies/{company_id}.json")


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_contacts(page: int = 1, per_page: int = 25) -> dict | list:
    """List all contacts."""
    return await client.get("/contacts.json", {"page": page, "per_page": per_page})


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
async def get_caller_lists(page: int = 1, per_page: int = 25) -> dict | list:
    """List all caller lists."""
    return await client.get("/caller_lists.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_caller_list(caller_list_id: int) -> dict:
    """Get a single caller list by ID."""
    return await client.get(f"/caller_lists/{caller_list_id}.json")


@mcp.tool()
async def get_caller_list_numbers(caller_list_id: int, page: int = 1, per_page: int = 25) -> dict | list:
    """List phone numbers in a caller list."""
    return await client.get(
        f"/caller_lists/{caller_list_id}/numbers.json",
        {"page": page, "per_page": per_page},
    )


# ---------------------------------------------------------------------------
# Suppressed Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_suppressed_numbers(page: int = 1, per_page: int = 25) -> dict | list:
    """List all suppressed numbers."""
    return await client.get("/suppressed_numbers.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_suppressed_number(suppressed_number_id: int) -> dict:
    """Get a single suppressed number by ID."""
    return await client.get(f"/suppressed_numbers/{suppressed_number_id}.json")


# ---------------------------------------------------------------------------
# Static Caller Numbers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_static_caller_numbers(page: int = 1, per_page: int = 25) -> dict | list:
    """List all static caller numbers."""
    return await client.get("/static_caller_numbers.json", {"page": page, "per_page": per_page})


# ---------------------------------------------------------------------------
# Target Groups
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_target_groups(page: int = 1, per_page: int = 25) -> dict | list:
    """List all target groups."""
    return await client.get("/target_groups.json", {"page": page, "per_page": per_page})


@mcp.tool()
async def get_target_group(target_group_id: int) -> dict:
    """Get a single target group by ID."""
    return await client.get(f"/target_groups/{target_group_id}.json")


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
    import argparse

    parser = argparse.ArgumentParser(description="Retreaver read-only MCP server")
    parser.add_argument("--port", type=int, default=8001, help="Port for SSE transport (default: 8001)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    args = parser.parse_args()

    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
