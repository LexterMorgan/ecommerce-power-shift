# SQLite deprecated

The Gate 7B dashboard data layer previously used
`ecommerce_power_shift.db` (SQLite).

**PostgreSQL is now the canonical project database.**

Do not recreate or consume a SQLite `.db` file for this project.
Rebuild with:

```bash
python3 scripts/build_dashboard_sql.py
```

Connection (override with `DATABASE_URL`):
`postgresql://localhost:5432/ecommerce_power_shift`
