from paramiko import SSHClient, AutoAddPolicy
from rich import print, pretty, inspect
pretty.install()

client = SSHClient()
#LOAD HOST KEYS
client.load_system_host_keys()

#Known_host policy
client.set_missing_host_key_policy(AutoAddPolicy())


#client.connect('host', username='username', password='password')
client.connect('10.31.81.2', username='ubnt', password='why1not2', look_for_keys=False,
               allow_agent=False)


# Run a command (execute PHP interpreter)
#client.exec_command('hostname')
stdin, stdout, stderr = client.exec_command('10.31.81.2')
print(type(stdin))
print(type(stdout))
print(type(stderr))

# Optionally, send data via STDIN, and shutdown when done
stdin.write('show ?\n')
# poe opmode shutdown
# poe opmode auto
stdin.channel.shutdown_write()

# Print output of command. Will wait for command to finish.
print(f'STDOUT: {stdout.read().decode("utf8")}')
print(f'STDERR: {stderr.read().decode("utf8")}')

# Get return code from command (0 is default for success)
print(f'Return code: {stdout.channel.recv_exit_status()}')

# Because they are file objects, they need to be closed
stdin.close()
stdout.close()
stderr.close()

# Close the client itself
client.close()
