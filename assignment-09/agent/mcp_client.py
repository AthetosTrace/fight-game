"""Minimal MCP client for the Unreal ModelContextProtocol plugin.

Speaks JSON-RPC over the plugin's Streamable-HTTP transport at
http://127.0.0.1:8000/mcp.

Why a hand-rolled socket transport instead of urllib
----------------------------------------------------
The plugin answers every ``tools/call`` with ``text/event-stream`` over a
keep-alive connection and sends no Content-Length. ``urllib`` reads that as a
zero-byte body and returns an empty result, while the editor log cheerfully
reports ``Running tool: '...'``. Reading the socket directly and parsing the SSE
frames ourselves is what actually works. Discovered 2026-08-24 while bringing up
the Assignment 09 harness; recorded here so nobody re-derives it.

Tool search is enabled on the server, so ``tools/list`` returns only three
meta-tools (list_toolsets, describe_toolset, call_tool). Real editor verbs are
reached through ``call_tool``. See CLAUDE.md "Two traps".

This client is READ-ONLY by contract: the adversarial QA agent samples state and
injects input. It never edits an asset. See ORACLE.md section 5.
"""

from __future__ import annotations

import json
import socket
from typing import Any

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_PATH = "/mcp"

PROTOCOL_VERSION = "2025-06-18"
CLIENT_INFO = {"name": "ascendant-adversarial-qa", "version": "1.0"}


class McpError(RuntimeError):
    """A JSON-RPC error, or a transport failure talking to the editor."""


class McpClient:
    """One MCP session against a running Unreal editor."""

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        path: str = DEFAULT_PATH,
        timeout: float = 120.0,
    ) -> None:
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.session_id: str | None = None
        self._next_id = 0
        self._initialized = False

    # ---- transport -----------------------------------------------------

    def _request(self, payload: dict, expect_id: int | None) -> dict:
        """POST one JSON-RPC message; return the matching response object."""
        body = json.dumps(payload)
        lines = [
            f"POST {self.path} HTTP/1.1",
            f"Host: {self.host}:{self.port}",
            "Content-Type: application/json",
            "Accept: application/json, text/event-stream",
            "Connection: keep-alive",
            f"Content-Length: {len(body.encode('utf-8'))}",
        ]
        if self.session_id:
            lines.append(f"Mcp-Session-Id: {self.session_id}")
        raw = ("\r\n".join(lines) + "\r\n\r\n" + body).encode("utf-8")

        try:
            sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        except OSError as exc:
            raise McpError(
                f"cannot reach the editor at {self.host}:{self.port} - is it open "
                f"and did ModelContextProtocol.StartServer run? ({exc})"
            ) from exc

        with sock:
            sock.sendall(raw)
            sock.settimeout(self.timeout)
            buf = b""
            header_done = False

            while True:
                try:
                    chunk = sock.recv(65536)
                except socket.timeout as exc:
                    raise McpError(
                        f"editor did not answer within {self.timeout:.0f}s - it may be "
                        f"compiling shaders or blocked on a modal dialog"
                    ) from exc
                if not chunk:
                    break
                buf += chunk

                if not header_done and b"\r\n\r\n" in buf:
                    head, _, rest = buf.partition(b"\r\n\r\n")
                    self._absorb_session_id(head)
                    buf = rest
                    header_done = True

                if header_done and expect_id is not None:
                    found = self._scan_frames(buf, expect_id)
                    if found is not None:
                        return found

                # A notification expects no reply; one flush is enough.
                if header_done and expect_id is None:
                    return {}

            if expect_id is None:
                return {}
            found = self._scan_frames(buf, expect_id)
            if found is not None:
                return found
            raise McpError(
                f"no response frame for id {expect_id}; "
                f"got {len(buf)} bytes: {buf[:300]!r}"
            )

    def _absorb_session_id(self, head: bytes) -> None:
        for line in head.decode("utf-8", errors="replace").splitlines():
            name, _, value = line.partition(":")
            if name.strip().lower() == "mcp-session-id":
                self.session_id = value.strip()

    @staticmethod
    def _scan_frames(buf: bytes, expect_id: int) -> dict | None:
        """Return the response object carrying the given JSON-RPC id, if present.

        The plugin is inconsistent about framing: ``initialize`` comes back as
        pretty-printed plain JSON, while ``tools/call`` comes back as SSE
        ``data:`` frames. Handle both rather than assuming either.
        """
        text = buf.decode("utf-8", errors="replace")

        # Plain-JSON body (initialize, and anything else not streamed).
        stripped = text.strip()
        if stripped.startswith("{"):
            try:
                msg = json.loads(stripped)
            except json.JSONDecodeError:
                pass  # body still arriving
            else:
                if msg.get("id") == expect_id:
                    return msg

        # SSE frames (tools/call).
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            blob = line[5:].strip()
            if not blob:
                continue
            try:
                msg = json.loads(blob)
            except json.JSONDecodeError:
                continue  # a partial frame; more bytes are still arriving
            if msg.get("id") == expect_id:
                return msg
        return None

    def _rpc(self, method: str, params: dict | None = None) -> dict:
        self._next_id += 1
        rid = self._next_id
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            payload["params"] = params

        msg = self._request(payload, expect_id=rid)
        if "error" in msg:
            err = msg["error"]
            raise McpError(f"{method} failed [{err.get('code')}]: {err.get('message')}")
        return msg.get("result", {})

    def _notify(self, method: str, params: dict | None = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        self._request(payload, expect_id=None)

    # ---- lifecycle -----------------------------------------------------

    def connect(self) -> dict:
        """Run the initialize handshake. Returns the server's capabilities."""
        if self._initialized:
            return {}
        result = self._rpc(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": CLIENT_INFO,
            },
        )
        self._notify("notifications/initialized")
        self._initialized = True
        return result

    # ---- discovery -----------------------------------------------------

    def list_tools(self) -> list[dict]:
        return self._rpc("tools/list").get("tools", [])

    def call(self, name: str, arguments: dict | None = None) -> dict:
        return self._rpc("tools/call", {"name": name, "arguments": arguments or {}})

    # ---- the three meta-tools -----------------------------------------

    def list_toolsets(self) -> str:
        return text_of(self.call("list_toolsets"))

    def describe_toolset(self, toolset_name: str) -> str:
        return text_of(self.call("describe_toolset", {"toolset_name": toolset_name}))

    def call_tool(
        self,
        tool_name: str,
        arguments: dict | None = None,
        toolset_name: str | None = None,
        autofill: bool = True,
    ) -> str:
        """Reach a real editor verb through the call_tool meta-tool.

        The plugin rejects a call unless every property that lacks an explicit
        ``default`` in the schema is present - even when the value is an empty
        string or list, and even when the parameter is conceptually optional.
        With ``autofill`` on we read the schema once, cache it, and supply those
        empties so callers only pass what they actually care about.
        """
        args: dict[str, Any] = {"tool_name": tool_name}
        if toolset_name:
            args["toolset_name"] = toolset_name

        payload = dict(arguments or {})
        if autofill and toolset_name:
            payload = self._autofill(toolset_name, tool_name, payload)
        if payload:
            args["arguments"] = payload
        return text_of(self.call("call_tool", args))

    # ---- schema cache --------------------------------------------------

    def toolset_schema(self, toolset_name: str) -> dict[str, dict]:
        """Return {short_tool_name: inputSchema} for a toolset, cached."""
        cache = getattr(self, "_schema_cache", None)
        if cache is None:
            cache = {}
            self._schema_cache = cache
        if toolset_name not in cache:
            raw = self.describe_toolset(toolset_name)
            try:
                described = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise McpError(f"could not parse toolset {toolset_name}: {raw[:200]}") from exc
            cache[toolset_name] = {
                tool["name"].rsplit(".", 1)[-1]: tool.get("inputSchema", {})
                for tool in described.get("tools", [])
            }
        return cache[toolset_name]

    def _autofill(self, toolset_name: str, tool_name: str, given: dict) -> dict:
        schema = self.toolset_schema(toolset_name).get(tool_name)
        if not schema:
            return given
        filled = dict(given)
        for prop, spec in (schema.get("properties") or {}).items():
            if prop in filled or "default" in spec:
                continue
            filled[prop] = _empty_for(spec)
        return filled


def _empty_for(spec: dict) -> Any:
    """The plugin's idea of 'absent' for a property with no declared default."""
    kind = spec.get("type")
    if kind == "string":
        return ""
    if kind == "array":
        return []
    if kind == "boolean":
        return False
    if kind in ("number", "integer"):
        return 0
    return None


def text_of(result: dict) -> str:
    """Flatten an MCP tool result into plain text."""
    if not isinstance(result, dict):
        return str(result)
    chunks: list[str] = []
    for item in result.get("content", []) or []:
        if isinstance(item, dict) and item.get("type") == "text":
            chunks.append(item.get("text", ""))
        else:
            chunks.append(json.dumps(item))
    if not chunks and result:
        return json.dumps(result)
    return "\n".join(chunks)


if __name__ == "__main__":
    client = McpClient()
    client.connect()
    print(f"session: {client.session_id}")
    print(client.list_toolsets())
