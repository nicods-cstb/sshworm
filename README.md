# sshworm
Tunnel ssh with python : simple and fast

## Usage
```python
    tunnel_conf = dict(
        ssh_config_name="example_config_in .ssh/config",
        local_port=5999,
        remote_forwarded_host="localhost",
        remote_forwarded_port=5432
    )
    pg_service = "pg_example_service"

    with create_worm(**tunnel_conf) as worm:

        assert worm is not None

         # to use pg services, create a pg_service.conf file in HOME
         # (https://www.postgresql.org/docs/current/libpq-pgservice.html)
        engine = sqlalchemy.create_engine(f"postgresql:///?service={pg_service}")

        with engine.connect() as conn:

            assert pandas.read_sql("SELECT 1 as s;", conn)["s"][0] == 1
    
        time.sleep(3)

        with engine.connect() as conn:

            assert pandas.read_sql("SELECT 3 as s;", conn)["s"][0] == 3

    assert True
```
