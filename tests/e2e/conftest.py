"""Fixtures for end-to-end tests.

These tests exercise the *whole* SDK stack over a real TCP socket: the public
client classes, the resource adapters, the generated low-level client, the
``httpx`` transport, the event hooks that implement per-request authentication
and header/timeout overrides, and the error translation layer.

Nothing is mocked or patched. The only substitution is the server on the other
end of the socket: a stdlib :class:`http.server.ThreadingHTTPServer` that serves
scripted responses and records every request it receives, so assertions can be
made about exactly what went out on the wire.
"""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import pytest

# A minimal but complete DataSourceLogin payload accepted by the generated models.
LOGIN_PAYLOAD: dict[str, Any] = {
    "type": "ds_login",
    "login_id": "login_abc123",
    "login_type": "oauth2",
    "username": "user@example.com",
    "display_name": "Example User",
    "ds_info": {"ds_id": "GAWA", "name": "Google Analytics 4"},
    "default_scopes": ["read_data"],
    "additional_scopes": [],
    "auth_time": "2026-01-01T00:00:00Z",
    "auth_user_info": {"user_id": "user_1", "email": "user@example.com"},
    "expiry_time": "2026-12-01T00:00:00Z",
    "revoked_time": None,
    "is_refreshable": True,
}

#: Response body for ``GET /ds/logins``.
LOGINS_LIST_BODY: dict[str, Any] = {"data": [LOGIN_PAYLOAD]}

#: Response body for ``GET /ds/login/{login_id}``.
LOGIN_GET_BODY: dict[str, Any] = {"data": LOGIN_PAYLOAD}


@dataclass(frozen=True)
class RecordedRequest:
    """A request as the server actually received it.

    Attributes:
        method: HTTP method, upper-case.
        path: Request path including the query string.
        headers: Request headers with lower-cased names.
        body: Raw request body bytes.
        client_port: Source port of the connection, used to prove pool reuse.
    """

    method: str
    path: str
    headers: dict[str, str]
    body: bytes
    client_port: int

    @property
    def authorization(self) -> str | None:
        """The ``Authorization`` header value, if the request carried one."""
        return self.headers.get("authorization")

    @property
    def bearer_token(self) -> str | None:
        """The bare bearer token, with the ``Bearer`` scheme stripped."""
        value = self.authorization
        if value is None or not value.lower().startswith("bearer "):
            return value
        return value[len("bearer ") :]

    def json(self) -> Any:
        """Decode the request body as JSON.

        Returns:
            The decoded payload, or ``None`` when the body is empty.
        """
        return json.loads(self.body) if self.body else None


@dataclass
class ScriptedResponse:
    """A response the mock server should return.

    Attributes:
        status: HTTP status code to send.
        json_body: Payload to serialize as JSON. Ignored when ``raw_body`` is set.
        headers: Extra response headers.
        delay: Seconds to sleep before responding, used to trigger real timeouts.
        raw_body: Exact body bytes, bypassing JSON serialization.
    """

    status: int = 200
    json_body: Any = None
    headers: dict[str, str] = field(default_factory=dict)
    delay: float = 0.0
    raw_body: bytes | None = None

    def body_bytes(self) -> bytes:
        """Return the response body as bytes."""
        if self.raw_body is not None:
            return self.raw_body
        if self.json_body is None:
            return b""
        return json.dumps(self.json_body).encode()


class MockAPIServer:
    """A real HTTP server that serves scripted responses and records requests.

    Routes are keyed by path (query strings are ignored when matching). Each route
    holds a queue of responses; once the queue is down to its final entry, that
    entry is served for every subsequent request, which keeps repeat-call tests
    simple.

    Example:
        ```python
        server.route("/ds/logins", ScriptedResponse(json_body={"data": []}))
        client = SupermetricsClient(api_key="k", base_url=server.base_url)
        client.logins.list()
        assert server.last_request.bearer_token == "k"
        ```
    """

    def __init__(self) -> None:
        """Start the server on an ephemeral loopback port."""
        self._routes: dict[str, list[ScriptedResponse]] = {}
        self._requests: list[RecordedRequest] = []
        self._lock = threading.Lock()
        self._default = ScriptedResponse(status=404, json_body={"error": {"code": "NOT_FOUND", "message": "no route"}})

        server = self

        class _Handler(BaseHTTPRequestHandler):
            # HTTP/1.1 keeps connections alive, so tests can prove pool reuse.
            protocol_version = "HTTP/1.1"

            def _handle(self) -> None:
                try:
                    self._respond()
                except (BrokenPipeError, ConnectionResetError):
                    # Expected when a timeout test abandons the request mid-flight.
                    self.close_connection = True

            def _respond(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                server._record(
                    RecordedRequest(
                        method=self.command,
                        path=self.path,
                        headers={k.lower(): v for k, v in self.headers.items()},
                        body=body,
                        client_port=self.client_address[1],
                    )
                )
                scripted = server._next_response(self.path)
                if scripted.delay:
                    time.sleep(scripted.delay)
                payload = scripted.body_bytes()
                self.send_response(scripted.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                for key, value in scripted.headers.items():
                    self.send_header(key, value)
                self.end_headers()
                if payload:
                    self.wfile.write(payload)

            do_GET = _handle
            do_POST = _handle
            do_PUT = _handle
            do_PATCH = _handle
            do_DELETE = _handle

            def log_message(self, format: str, *args: Any) -> None:
                """Silence the default stderr access log."""

            def handle_one_request(self) -> None:
                """Handle one request, swallowing disconnects from abandoned calls."""
                try:
                    super().handle_one_request()
                except (BrokenPipeError, ConnectionResetError):
                    self.close_connection = True

        class _Server(ThreadingHTTPServer):
            def handle_error(self, request: Any, client_address: Any) -> None:
                """Swallow the traceback a client disconnect would otherwise print."""

        self._httpd = _Server(("127.0.0.1", 0), _Handler)
        self._httpd.daemon_threads = True
        # A short poll interval keeps shutdown() from blocking for the default 0.5s,
        # which across ~90 tests and six CI legs is most of the suite's wall clock.
        self._thread = threading.Thread(target=self._httpd.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        self._thread.start()

    @property
    def base_url(self) -> str:
        """Base URL to hand to a Supermetrics client."""
        host, port = self._httpd.server_address[:2]
        return f"http://{host}:{port}"

    @property
    def requests(self) -> list[RecordedRequest]:
        """A snapshot of every request received so far, in arrival order."""
        with self._lock:
            return list(self._requests)

    @property
    def last_request(self) -> RecordedRequest:
        """The most recently received request.

        Raises:
            AssertionError: If no request has been received.
        """
        received = self.requests
        assert received, "no request was received by the mock server"
        return received[-1]

    def route(self, path: str, *responses: ScriptedResponse) -> None:
        """Register the responses to serve for ``path``.

        Args:
            path: Request path to match, without a query string.
            responses: Responses to serve in order. The last one repeats.
        """
        with self._lock:
            self._routes[path] = list(responses) or [ScriptedResponse()]

    def set_default(self, response: ScriptedResponse) -> None:
        """Set the response served for paths with no registered route.

        Args:
            response: The fallback response.
        """
        self._default = response

    def clear(self) -> None:
        """Forget all recorded requests."""
        with self._lock:
            self._requests.clear()

    def stop(self) -> None:
        """Shut the server down and join its thread."""
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)

    def _record(self, request: RecordedRequest) -> None:
        with self._lock:
            self._requests.append(request)

    def _next_response(self, path: str) -> ScriptedResponse:
        key = path.split("?", 1)[0]
        with self._lock:
            queue = self._routes.get(key)
            if not queue:
                return self._default
            return queue.pop(0) if len(queue) > 1 else queue[0]


@pytest.fixture
def api_server() -> Iterator[MockAPIServer]:
    """Provide a running :class:`MockAPIServer` for one test."""
    server = MockAPIServer()
    try:
        yield server
    finally:
        server.stop()


@pytest.fixture
def logins_server(api_server: MockAPIServer) -> MockAPIServer:
    """A server with the two login routes wired to successful responses."""
    api_server.route("/ds/logins", ScriptedResponse(json_body=LOGINS_LIST_BODY))
    api_server.route("/ds/login/login_abc123", ScriptedResponse(json_body=LOGIN_GET_BODY))
    return api_server
