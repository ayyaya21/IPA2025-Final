from netmiko import ConnectHandler
from pprint import pprint
import paramiko
import re

# Fix KEX & preferred keys for older devices
paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
)
paramiko.transport.Transport._preferred_keys = (
    'ssh-rsa',
)

device_params_template = {
    "device_type": "cisco_ios",
    "username": "admin",
    "password": "cisco",
    'port': 22,
    'conn_timeout': 20,
    'timeout': 30,
}

def read_motd(device_ip):
    """Connect to device via Netmiko and read the current MOTD."""
    device_params = device_params_template.copy()
    device_params['host'] = device_ip

    try:
        with ConnectHandler(**device_params) as ssh:
            output = ssh.send_command("show running-config | include banner motd")
            if output:
                motd_text = output.replace("banner motd", "").replace("^C", "").replace("^C", "").strip()
                return motd_text
            else:
                return "Error: No MOTD Configured"
    except Exception as e:
        return "Error: No MOTD Configured"
