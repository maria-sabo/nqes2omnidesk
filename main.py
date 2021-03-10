import sshtunnel
import config
from db_request import request_new_issues_from_db

if __name__ == '__main__':
    with sshtunnel.SSHTunnelForwarder(
            (config.ssh_host_url, config.ssh_port),
            ssh_private_key=config.ssh_path_to_key,
            ssh_username=config.ssh_username,
            remote_bind_address=('localhost', config.postgres_port),
            local_bind_address=('localhost', config.ssh_port)) as server:
        server.start()
        print(request_new_issues_from_db())
