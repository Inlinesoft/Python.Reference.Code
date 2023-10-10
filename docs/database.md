### Alembic - autogenerate tables from domain entities
alembic revision --autogenerate -m "Init"

### Loading dev data
loaddevdata


### Dump UAT database into Local [Run inside db container]

1. ssh into the postgres Container
2. `cd ~`
3. `pg_dump --dbname=postgresql://postgres:<get from password store>@<hostname>:5432/loader | psql $DB_URL`