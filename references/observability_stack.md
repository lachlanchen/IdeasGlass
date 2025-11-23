# Observability Stack: Grafana + Loki + Promtail

This brings serial, backend, and (optional) frontend logs into a single UI.

## Layout

- `ops/observability/docker-compose.yml` — starts Grafana (3000), Loki (3100), Promtail
- `ops/observability/promtail-config.yml` — tails local log folders:
  - `logs/ideasglass-serial/*.log` (serial logger)
  - `logs/ideasglass-backend/*.log` (backend logger)
  - `logs/frontend/*.log` (optional frontend log file)
- `ops/observability/loki-config.yml` — local filesystem storage for Loki (14‑day retention)
- `ops/observability/grafana/provisioning/datasources/loki.yaml` — prewired Loki datasource

## Run

```bash
cd ops/observability
docker compose up -d
```

Open Grafana: http://localhost:3000 (admin / admin)

Explore → Loki → enter a query like:

```
{app="ideasglass"}
```

or filter by source:

```
{app="ideasglass",source="serial"}
{app="ideasglass",source="backend"}
{app="ideasglass",source="frontend"}
```

## Feeding logs

- Serial: run `backend/bridge/tools/serial_logger.py` (writes to `logs/ideasglass-serial`).
- Backend: run `backend/bridge/tools/backend_logger.py` (writes to `logs/ideasglass-backend`).
- Frontend: if desired, append browser logs to files under `logs/frontend/` or add a tiny POST endpoint in FastAPI that writes to a log file in that directory. Promtail will pick them up automatically.

## Stop / Clean

```bash
docker compose down
docker volume rm ops_observability_grafana-storage ops_observability_loki-data # optional wipe
```

## Notes

- Promtail stores read offsets in `ops/observability/promtail-positions.yaml` (created at runtime).
- You can adjust Loki retention in `loki-config.yml` (`retention_period`).
