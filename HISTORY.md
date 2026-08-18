# History

## 0.3.0-beta1 (2026-06-09)

* Add Connector Builder resource with full CRUD support: create, get, list, update, delete connectors
* Add Connector Builder Secrets resource: create, list, update, delete encrypted secrets
* Add Connector Builder Logs resource: list and get connector execution logs
* Add Connector Builder Logo support: get and upload connector logos
* Add `connector_builder_flow.py` example with `--base-url` flag for local dev testing
* Fix OpenAPI filter script: resolve transitive schema dependencies and bare `$ref` rewriting

## 0.2.0-beta1 (2026-03-26)

* Add Backfills resource with full CRUD support: create, get latest, list incomplete, and cancel backfills ([#16](../../pull/16))
* Add public documentation link and fix broken links ([#17](../../pull/17))
* Remove broken documentation link ([#13](../../pull/13))
* Security: bump `actions/download-artifact` from 7 to 8 ([#14](../../pull/14))
* Security: bump `actions/upload-artifact` from 6 to 7 ([#15](../../pull/15))

## 0.1.0 (2025-10-28)

* First release on PyPI.
