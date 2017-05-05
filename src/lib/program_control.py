from .emulate_manager import EmulateManager


class ProgramControl:
    '''Class controlling program flow, methods invoking'''
    args = None

    def __init__(self):
        pass

    def run(self, parser_args):
        self.set_args(parser_args)
        parser_args.func()

    def mount(self):
        emulator = EmulateManager(*self.args)
        emulator.mount()

        print('Successfully mounted')

    def umount(self):
        emulator = EmulateManager(*self.args)
        emulator.umount()

        print('Successfully umounted')

    def spawn_shell(self):
        emulator = EmulateManager(*self.args)
        emulator.spawn_chroot()

    def set_args(self, parser_args):
        args = list()
        args.append(parser_args.path)
        if parser_args.mnt:
            args.append(parser_args.mnt)

        self.args = args
