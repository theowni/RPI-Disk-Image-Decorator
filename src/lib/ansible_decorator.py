import os
from .emulate_manager import EmulateManager


PLAYBOOKS_DIR = '/playbooks'


class AnsibleDecorator:
    def __init__(self, emulate_manager):
        if not emulate_manager.is_mounted():
            raise Exception('First, mount image!')

        self.emulator = emulate_manager

    def setup_env(self):
        print('-------------------\nUpdate packages list\n-------------------')
        self.emulator.run_command_remote('apt-get update')
        print('\n-------------------\nInstall ansible\n-------------------')
        self.emulator.run_command_remote('apt-get install ansible -y')
        self.emulator.run_command_remote('mkdir -p {}'.format(
            PLAYBOOKS_DIR
        ))

    def run_playbook(self, playbook_path):
        '''Run specified playbook by its path'''

        self.emulator.run_command_remote(
            'ansible-playbook -i "localhost," -c local {}'.format(
                playbook_path
            )
        )

    def upload_playbook(self, playbook_path):
        '''Uploads specified playbook'''

        playbook_name = os.path.basename(playbook_path)
        target = os.path.join(PLAYBOOKS_DIR, playbook_name)
        self.emulator.upload_file(playbook_path, target)

        return target
