from .settings_manager import SettingsManager
from .emulate_manager import EmulateManager
from .ansible_decorator import AnsibleDecorator


class ProgramControl:
    '''Class controlling program flow, methods invoking'''

    def __init__(self):
        self.settings = SettingsManager()

    def run(self, parser_args):
        parser_args.func(parser_args)

    def mount(self, parser_args):
        emulator = self.get_emulator(parser_args)
        emulator.mount()

        self.settings.set('IMG_PATH', parser_args.path)
        if parser_args.mnt:
            self.settings.set('MNT_PATH', parser_args.mnt)

        print('Successfully mounted')

    def umount(self, parser_args):
        emulator = self.get_emulator(parser_args)
        emulator.umount()

        print('Successfully umounted')

    def spawn_shell(self, parser_args):
        emulator = self.get_emulator(parser_args)
        emulator.spawn_chroot()

    def run_playbook(self, parser_args):
        emulator = self.get_emulator(parser_args)
        ansible = AnsibleDecorator(emulator)
        ansible.setup_env()

        path = parser_args.playbook_path
        print('\n-------------------\nUpload playbook\n-------------------\n')
        remote_path = ansible.upload_playbook(path)
        print('-------------------\nRun playbook\n-------------------')
        ansible.run_playbook(remote_path)

    def get_emulator(self, parser_args):
        args = list()
        count = 0
        if parser_args.path:
            count = 1
            args.append(parser_args.path)
        if parser_args.mnt:
            count = 2
            args.append(parser_args.mnt)

        if count == 0:
            args.append(self.settings.get('IMG_PATH'))

        if count < 2:
            args.append(self.settings.get('MNT_PATH'))

        emulator = EmulateManager(*args)
        return emulator
