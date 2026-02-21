"""Shared async HTTP client for the Retreaver API."""

from __future__ import annotations

import os
import re

import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://api.retreaver.com"


class RetreaverClient:
    """Thin wrapper around httpx.AsyncClient that injects auth params."""

    def __init__(self) -> None:
        self.api_key = os.environ["RETREAVER_API_KEY"]
        self.company_id = os.environ["RETREAVER_COMPANY_ID"]
        self.base_url = os.environ.get("RETREAVER_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self._client: httpx.AsyncClient | None = None

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    def _auth_params(self) -> dict[str, str]:
        return {"api_key": self.api_key, "company_id": self.company_id}

    def _url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    async def get(self, path: str, params: dict | None = None) -> dict | list:
        client = await self._ensure_client()
        merged = {**self._auth_params(), **(params or {})}
        resp = await client.get(self._url(path), params=merged)
        return self._handle(resp)

    async def post(self, path: str, json: dict | None = None, params: dict | None = None) -> dict | list:
        client = await self._ensure_client()
        merged_params = {**self._auth_params(), **(params or {})}
        resp = await client.post(self._url(path), json=json, params=merged_params)
        return self._handle(resp)

    async def put(self, path: str, json: dict | None = None, params: dict | None = None) -> dict | list:
        client = await self._ensure_client()
        merged_params = {**self._auth_params(), **(params or {})}
        resp = await client.put(self._url(path), json=json, params=merged_params)
        return self._handle(resp)

    async def delete(self, path: str, params: dict | None = None) -> dict | list | str:
        client = await self._ensure_client()
        merged = {**self._auth_params(), **(params or {})}
        resp = await client.delete(self._url(path), params=merged)
        return self._handle(resp)

    @staticmethod
    def _parse_link_header(header: str) -> dict[str, int]:
        """Extract page numbers from a Link header.

        Example header:
            <https://api.retreaver.com/campaigns.json?page=2&per_page=25>; rel="next",
            <https://api.retreaver.com/campaigns.json?page=10&per_page=25>; rel="last"

        Returns e.g. {"next": 2, "last": 10}
        """
        pagination: dict[str, int] = {}
        for match in re.finditer(r'<[^>]*[?&]page=(\d+)[^>]*>;\s*rel="(\w+)"', header):
            page_num, rel = match.group(1), match.group(2)
            pagination[rel] = int(page_num)
        return pagination

    @staticmethod
    def _handle(resp: httpx.Response) -> dict | list | str:
        if resp.status_code >= 400:
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise RuntimeError(f"Retreaver API error {resp.status_code}: {body}")
        if not resp.content:
            return {"ok": True, "status": resp.status_code}
        try:
            body = resp.json()
        except Exception:
            return resp.text

        link_header = resp.headers.get("link", "")
        if link_header and isinstance(body, list):
            pagination = RetreaverClient._parse_link_header(link_header)
            if pagination:
                return {"data": body, "pagination": pagination}

        return body

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
