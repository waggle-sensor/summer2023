from paramiko import SSHClient, AutoAddPolicy
from rich import print, pretty, inspect
pretty.install()

client = SSHClient()
#LOAD HOST KEYS
#client.load_host_keys('~/.ssh/known_hosts')
# client.load_host_keys('/home/waggle/.ssh/known_hosts')
client.load_system_host_keys()

#Known_host policy
client.set_missing_host_key_policy(AutoAddPolicy())


#client.connect('10.31.81.2', username='ubnt', password='password')
client.connect('10.31.81.2', username='ubnt', password='')


# Run a command (execute PHP interpreter)
#client.exec_command('hostname')
stdin, stdout, stderr = client.exec_command('10.31.81.2')
print(type(stdin))
print(type(stdout))
print(type(stderr))

# Optionally, send data via STDIN, and shutdown when done
stdin.write('enable\nwhy1not2\n?\nq\nconfigure\ninterface 0/1\npoe opmode auto\n')
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
