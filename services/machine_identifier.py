# services/machine_identifier.py  # pylint: disable=duplicate-code
"""
This module is used to generate a unique identifier
for the machine that the application is running on.
"""
import uuid
import platform
import subprocess
import os
import hashlib


class MachineIdentifier:
    """
    This class generates a unique identifier for the machine
    that the application is running on. The identifier is
    generated based on the machine's hardware and software
    configuration.
    """
    def __init__(self):
        self.unique_id = self._generate_unique_id()

    def _generate_unique_id(self):
        """
        Generate a unique identifier for the machine.
        """
        system = platform.system()

        if system == 'Windows':
            return self._get_windows_uuid()
        elif system == 'Linux':
            return self._get_linux_machine_id()
        else:
            return self._get_generic_unique_id()

    def _get_windows_uuid(self):
        """
        Get the UUID of the machine on Windows.
        """
        try:
            output = subprocess.check_output('wmic csproduct get UUID', shell=True)
            uuid_str = output.decode().split('\n')[1].strip()
            return self._hash_string(uuid_str)
        except Exception as e:
            print(f'Error getting Windows UUID: {e}')
            return self._get_generic_unique_id()

    def _get_linux_machine_id(self):
        """
        Get the machine ID of the machine on Linux.
        """
        try:
            if os.path.exists('/etc/machine-id'):
                with open('/etc/machine-id', 'r') as f:
                    machine_id = f.read().strip()
                    return self._hash_string(machine_id)
            elif os.path.exists('/var/lib/dbus/machine-id'):
                with open('/var/lib/dbus/machine-id', 'r') as f:
                    machine_id = f.read().strip()
                    return self._hash_string(machine_id)
            else:
                return self._get_generic_unique_id()
        except Exception as e:
            print(f'Error getting Linux machine ID: {e}')
            return self._get_generic_unique_id()

    def _get_generic_unique_id(self):
        """
        Get a generic unique ID for the machine.
        """
        mac = uuid.getnode()
        system = platform.system()
        node = platform.node()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()

        unique_string = (
            f"{system}-{node}-{release}-"
            f"{version}-{machine}-{processor}-{mac}"
        )
        return self._hash_string(unique_string)

    def _hash_string(self, input_string):
        """
        Hash the input string using SHA-256.
        """
        return hashlib.sha256(input_string.encode()).hexdigest()

    def get_id(self):
        """
        Get the unique identifier for the machine.
        """
        return self.unique_id
