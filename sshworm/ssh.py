from subprocess import Popen, PIPE
import threading
import time
import requests


# f_list = glob.glob('./*bz2')
# cmds_list = [['./bunzip2_file.py', file_name] for file_name in f_list]
# procs_list = [Popen(cmd, stdout=PIPE, stderr=PIPE) for cmd in cmds_list]
# for proc in procs_list:
# 	proc.wait()


def open_ssh_tunnel_shell_command(ssh_config_name: str,
                      local_port: int,
                      remote_forwarded_host: str,
                      remote_forwarded_port: int) -> list[str]:
    return ["ssh",
            ssh_config_name,
            "-NL",
            f"{local_port}:{remote_forwarded_host}:{remote_forwarded_port}"
            ]

sub = Popen(
    open_ssh_tunnel_shell_command("my_ssh_config", 8080, "localhost", 8080),
    stdout=PIPE,
    stderr=PIPE
)

def thread_function():
        
    try:
        print(f"waiting1...{sub}")
        sub.wait(timeout=20)
        print(f"waiting2...{sub}")
    except:
        print(f"waiting3...{sub.poll()}")
        sub.terminate()
        print("END")

    time.sleep(5)

def open_thread():

    x = threading.Thread(target=thread_function, args=())
    
    x.start()
    time.sleep(3)
    print(f"sub: {sub}")    
    
    
    print(threading.active_count())
    
    time.sleep(1)
    
    resp = requests.get("http://localhost:8080")

    print(resp)
    
    for i in range(1, 10):
        time.sleep(1)
        print(i)
        
    sub.terminate()
