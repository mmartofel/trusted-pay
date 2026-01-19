#/bin/bash

export PAGER=cat

PGPASSWORD='postgres' psql -d trusted_pay -U postgres -h localhost -p 5432

