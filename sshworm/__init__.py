from subprocess import Popen, PIPE
import time
from typing import Optional

import logging



class ImpossibleException(Exception):
    pass


class BadPracticeException(Exception):
    pass


class _SshFastTunnel:

    def __init__(self,
                 ssh_config_name: str,
                 local_port: int,
                 remote_forwarded_host: str,
                 remote_forwarded_port: int):
        
        self.ssh_config_name = ssh_config_name
        self.local_port = local_port
        self.remote_forwarded_host = remote_forwarded_host
        self.remote_forwarded_port = remote_forwarded_port

        # state
        self.ssh_popen : Optional[Popen] = None

        # Log
        self._logger_ = logging.getLogger(__name__)

        # Constants
        self._ssh_command_timeout_: int = 36_000
    

    def _open_ssh_tunnel_shell_command(self) -> list[str]:
        return ["ssh",
            self.ssh_config_name,
            "-NL",
            f"{self.local_port}:{self.remote_forwarded_host}:{self.remote_forwarded_port}"
        ]

    def open(self):

        command = self._open_ssh_tunnel_shell_command()
        self._logger_.debug(f"openning tunnel...{self.ssh_popen}")

        self.ssh_popen = Popen(
            command,
            stdout=PIPE,
            stderr=PIPE
        )
        

    def close(self):
        self._logger_.debug(f"Closing tunnel on {self.ssh_config_name}")
        if self.ssh_popen is None:
                raise ImpossibleException("Trying to close a None sub")
        self.ssh_popen.terminate()
        self.ssh_popen = None


class create_worm:

    def __init__(self,
                 ssh_config_name: str,
                 local_port: int,
                 remote_forwarded_host: str,
                 remote_forwarded_port: int):
        
        self.ssh_config_name = ssh_config_name
        self.local_port = local_port
        self.remote_forwarded_host = remote_forwarded_host
        self.remote_forwarded_port = remote_forwarded_port

        # State
        self._proprely_call_in_with: bool = False
        self._tunnel: Optional[_SshFastTunnel] = None


    def __enter__(self):
        self._proprely_call_in_with = True
        self.open_tunnel()
        time.sleep(0.01)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._tunnel is None:
            raise ImpossibleException("Couldn't open tunnel but trying to close it")
        self._tunnel.close()

    def open_tunnel(self):
        if not self._proprely_call_in_with:
            raise BadPracticeException('Bad practice. Please use this class inside a "with" statement.'
                                       f' Ex: `with {self.__class__.__name__}() as worm:\\n worm.open_tunnel()'
                                       f'`')

        self._tunnel = _SshFastTunnel(
            self.ssh_config_name,
            self.local_port,
            self.remote_forwarded_host,
            self.remote_forwarded_port
        )
        self._tunnel.open()
