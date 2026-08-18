# Authentication & Transport

This guide covers how the SDK authenticates, how a single client can serve many concurrent
callers, and how to reach the HTTP metadata behind a response.

---

## Choosing a credential

Both `SupermetricsClient` and `SupermetricsAsyncClient` accept **exactly one** credential.
Passing none, or more than one, raises `SupermetricsClientError` (which is also a
`ValueError`) before any request is made.

### Static API key

```python
from supermetrics import SupermetricsClient

client = SupermetricsClient(api_key="api_live_abc123")
```

### OAuth bearer token

```python
client = SupermetricsClient(bearer_token="otok_abc123")
```

Tokens are opaque to the SDK. API keys, OAuth access tokens, RFC 8693 exchanged/delegated
tokens, and JWTs are all sent unchanged as `Authorization: Bearer <token>`. A value that
already carries the scheme (`"Bearer otok_abc123"`) is not prefixed twice, and surrounding
whitespace is trimmed.

The SDK does reject a credential it cannot legally send, rather than letting it fail as an
opaque server error: an empty or whitespace-only value, one containing a control character
(typically a newline from a line-wrapped file or a YAML block scalar), or one containing a
non-ASCII character (typically a smart quote or en dash pasted from a document) raises
`SupermetricsClientError`. Those messages never echo the credential, because the HTTP layer
would otherwise quote the whole value into an error that callers log.

### Dynamic token provider

Short-lived tokens expire. Rebuilding the client to pick up a new one throws away the
connection pool and the TLS session cache along with it. Instead, hand the client a
callable that is evaluated on **every** request:

```python
client = SupermetricsClient(token_provider=lambda: vault.current_access_token())
```

The async client additionally accepts a coroutine function:

```python
from supermetrics import SupermetricsAsyncClient


async def get_valid_token() -> str:
    return await oauth_service.get_access_token(team_id=123)


client = SupermetricsAsyncClient(token_provider=get_valid_token)
```

An `async def` provider passed to the **synchronous** client is rejected at construction
time rather than failing on the first request.

---

## Per-request overrides

Every resource method takes three keyword-only overrides, so one shared client can serve
concurrent callers that each bring their own credential and tracing context:

```python
transfer = client.logins.get(
    "login_abc123",
    auth_token="otok_this_caller",  # overrides the client credential
    headers={"X-Span-Id": "a8f3b2c9", "Idempotency-Key": "req-42"},
    timeout=120.0,  # seconds, or an httpx.Timeout
)
```

These are bound to context variables for the duration of the call only, and context
variables are isolated per thread and per asyncio task. Twelve concurrent tasks on one
pooled client will each send their own token, with no cross-contamination and without
opening twelve connections.

### Header precedence

Later entries win:

1. SDK defaults (`User-Agent: supermetrics-sdk/<version> python/<x.y>`)
2. Client-level `custom_headers`
3. The resolved `Authorization` header (`auth_token`, else the token provider, else the
   static credential)
4. Per-request `headers`

Merging is case-insensitive, so `{"x-team-id": ...}` replaces a client-level `X-Team-ID`.
Because per-request headers are applied last, passing `Authorization` there is a deliberate
escape hatch that overrides everything else.

Client-level `custom_headers`, by contrast, cannot set `Authorization`: the credential
always comes from `api_key`, `bearer_token`, or `token_provider`. Trying to set it there
emits a `UserWarning` and is ignored, because otherwise the same header set would send a
different credential depending on which mechanism was chosen.

### Ambient propagation

In an async web framework it is often cleaner to set the caller's context once, in
middleware, than to thread arguments through every layer:

```python
from supermetrics import current_auth_token, current_request_headers


@app.middleware("http")
async def bind_caller_context(request, call_next):
    token = current_auth_token.set(request.headers["authorization"].removeprefix("Bearer "))
    headers = current_request_headers.set({"X-Span-Id": request.state.span_id})
    try:
        return await call_next(request)
    finally:
        current_auth_token.reset(token)
        current_request_headers.reset(headers)
```

Any SDK call made while handling that request inherits the ambient values. An explicit
argument on a call still wins over the ambient one.

The `request_options()` context manager does the same thing for a block of code:

```python
from supermetrics import request_options

with request_options(auth_token="otok_abc", headers={"X-Span-Id": "s1"}):
    client.logins.list()
    client.accounts.list(ds_id="GAWA", login_usernames="user@example.com")
```

---

## Reading response metadata

Resource methods return parsed models. When you also need the status code, headers, or raw
payload — for tracing, rate-limit handling, or auditing — use `with_raw_response`. It
mirrors every method with an identical signature and returns an `ApiResponse[T]`:

```python
response = client.with_raw_response.logins.get("login_abc123")

response.status_code  # 200
response.data  # the DataSourceLogin the plain method would have returned
response.span_id  # X-Span-Id, for linking traces
response.request_id  # X-Request-Id, for support tickets
response.retry_after  # Retry-After in seconds, or None
response.headers  # the full httpx.Headers
response.raw_body  # bytes
response.json_body  # the decoded payload, or None if it was not JSON
```

The async client works the same way:

```python
response = await async_client.with_raw_response.logins.get("login_abc123")
```

> A few methods issue more than one HTTP request (`queries.execute` while polling,
> `logins.get_by_username` which lists first). For those, the envelope describes the last
> response.

---

## Error taxonomy

```
SupermetricsError
├── SupermetricsClientError        local configuration problems; also a ValueError
├── NetworkError                   timeout, connection refused, DNS, TLS
└── SupermetricsAPIError                           [alias: APIError]
    ├── SupermetricsAuthError       401            [alias: AuthenticationError]
    ├── SupermetricsForbiddenError  403
    ├── SupermetricsNotFoundError   404
    ├── SupermetricsValidationError 400 / 422      [alias: ValidationError]
    ├── SupermetricsRateLimitError  429
    └── SupermetricsServerError     5xx
```

Every `SupermetricsAPIError` carries `status_code`, `endpoint`, `headers`, `error_code`,
`error_message`, `details`, and `response_body`, plus the `retry_after`, `request_id`, and
`span_id` helper properties.

### Refreshing an expired token

A 401 exposes the upstream OAuth code, so a caller can tell "refresh and retry" apart from
"this credential will never work":

```python
from supermetrics import SupermetricsAuthError

try:
    logins = client.logins.list()
except SupermetricsAuthError as error:
    if error.error_code in ("ACCESS_TOKEN_INVALID", "ACCESS_TOKEN_EXPIRED"):
        credentials.refresh()
        logins = client.logins.list()
    else:
        raise
```

### Backing off on a 429

```python
from supermetrics import SupermetricsRateLimitError

try:
    result = client.queries.execute(...)
except SupermetricsRateLimitError as error:
    time.sleep(error.retry_after or 30)
```

### Compatibility note

`APIError`, `AuthenticationError`, and `ValidationError` are still importable and are now
aliases of `SupermetricsAPIError`, `SupermetricsAuthError`, and
`SupermetricsValidationError`. Because the specific HTTP errors now descend from
`APIError`, an `except APIError` clause placed **before** `except AuthenticationError` will
match authentication errors first. Order the specific clauses first:

```python
except SupermetricsAuthError:
    ...
except SupermetricsRateLimitError:
    ...
except APIError:        # everything else at the HTTP layer
    ...
```

---

## Timeouts

`timeout` at construction time sets the client default; `timeout` on a call overrides it
for that call only and does not leak into the next one:

```python
client = SupermetricsClient(api_key="api_k", timeout=30.0)

client.logins.list()  # 30s
client.queries.execute(..., timeout=300.0)  # 300s, for a long extraction
client.logins.list()  # 30s again
```

Timeouts surface as `NetworkError`, which has no `status_code` because no HTTP response was
received.

---

## Writing to the API safely

Adapters whose generated parser returns nothing on success — deletes, and updates that
answer `204 No Content` — verify the transport actually saw a success before reporting one.
A gateway `502` therefore raises `SupermetricsServerError`, rather than returning `None`
like a completed delete. Likewise, a response whose body does not match the documented
schema, or that carries a status the API specification does not describe for the operation,
is still classified by the status code the transport observed, so a recoverable `401` never
arrives as an unclassified error.
