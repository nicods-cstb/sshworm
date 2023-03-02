import time
import pandas
import sqlalchemy
from sshworm import create_worm

def test_tunnel():

    tunnel_conf = dict(
        ssh_config_name="example_config_in .ssh/config",
        local_port=5999,
        remote_forwarded_host="localhost",
        remote_forwarded_port=5432
    )
    pg_service = "pg_example_service"

    with create_worm(**tunnel_conf) as worm:

        assert worm is not None


        engine = sqlalchemy.create_engine(f"postgresql:///?service={pg_service}")

        with engine.connect() as conn:

            assert pandas.read_sql("SELECT 1 as s;", conn)["s"][0] == 1
    
        time.sleep(3)

        with engine.connect() as conn:

            assert pandas.read_sql("SELECT 3 as s;", conn)["s"][0] == 3

    assert True


if __name__ == '__main__':

    test_tunnel()