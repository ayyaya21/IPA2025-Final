import subprocess
import json
import re
def configure_motd(host, message):
    vars = { "motd_message": message }
    command = ['ansible-playbook', 'motd_playbook.yaml', "-e",json.dumps(vars) ,'--flush-cache']

    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    print(result)
    match = re.search(r'"msg":\s*"([^"]+)"', result)
    print(match.group(1))
    if 'ok=2' in result:
        return "Ok: success"
    else:
        return "Error: Ansible"
