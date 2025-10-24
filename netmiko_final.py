from netmiko import ConnectHandler
import paramiko
import re

paramiko.transport.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1',
)
paramiko.transport.Transport._preferred_keys = (
    'ssh-rsa',
)

username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "username": username,
    "password": password,
    'port': 22,
    'conn_timeout': 20,
    'timeout': 30,
}

def motd(host, message):
    router = device_params.copy()
    router["host"] = host
    try:
        connection = ConnectHandler(**router)
        connection.enable()
        connection.send_config_set([f"banner motd ^{message}^"])
        connection.save_config()
        connection.disconnect()
        return "Ok: success"
    except Exception as e:
        return f"Error: {str(e)}"

def get_motd(host):
    router = device_params.copy()
    router["host"] = host
    try:
        connection = ConnectHandler(**router)
        output = connection.send_command("show running-config | include banner motd")
        connection.disconnect()
        if output:
            match = re.search(r'\^(.+)\^', output)
            if match:
                return match.group(1)
        return "Error: No MOTD Configured"
    except Exception as e:
        return f"Error: {str(e)}"
