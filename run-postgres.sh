
podman run \
  --name trusted-pay-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=trusted_pay \
  -p 5432:5432 \
  -d postgres