from pathlib import Path


class BadPracticeException(Exception):
    pass


class _SshFastTunnel:

    def __init__(self,
                 ssh_host,
                 ssh_usr: str = "",
                 ssh_password: str = None,
                 ssh_private_key_path: Path = None,
                 ssh_port=22):

        self._ssh_host = ssh_host
        self._ssh_usr = ssh_usr
        self._ssh_password = ssh_password
        self._ssh_private_key_path = ssh_private_key_path
        self._ssh_port = ssh_port

    def open(self):
        print(f"Openning tunnel on {self._ssh_host}")

    def close(self):
        print(f"Closing tunnel on {self._ssh_host}")


class SshFastTunnelFactory:
    def __init__(self,
                 ssh_host,
                 ssh_usr: str = "",
                 ssh_password: str = None,
                 ssh_private_key_path: Path = None,
                 ssh_port=22):
        self._ssh_host = ssh_host
        self._ssh_usr = ssh_usr
        self._ssh_password = ssh_password
        self._ssh_private_key_path = ssh_private_key_path
        self._ssh_port = ssh_port

        self._proprely_call_in_with = False
        self._tunnel = None
        print("init Factory")

    def __enter__(self):
        self._proprely_call_in_with = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tunnel.close()

    def open_tunnel(self):
        if not self._proprely_call_in_with:
            raise BadPracticeException('Bad practice. Please use this class inside a "with" statement.'
                                       f' Ex: `with {self.__class__.__name__}() as tunnel_fact:\\n tunnel_fact.open_tunnel()'
                                       f'`')

        self._tunnel = _SshFastTunnel(
            self._ssh_host,
            self._ssh_usr,
            self._ssh_password,
            self._ssh_private_key_path,
            self._ssh_port)

        return self._tunnel