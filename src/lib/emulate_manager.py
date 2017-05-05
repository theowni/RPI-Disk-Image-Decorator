import subprocess
import os

PATH = os.path.dirname(os.path.realpath(__file__))
MNT_PATH = '/mnt/rpiem'


class EmulateManager:
    '''Managing mounting points and emulation process'''

    def __init__(self, img_path, mnt_path=MNT_PATH):
        '''Prepare settings and os env'''
        self.img_path = img_path
        self.mnt_path = mnt_path

    def mount(self):
        '''Setup mounting point and prepare filesystems'''

        self.run_command("sudo kpartx -asv {}".format(self.img_path))
        self.run_command("sudo mkdir -p {}".format(self.mnt_path))
        self.run_command("sudo mount /dev/mapper/loop0p2 {}".format(
            self.mnt_path))
        self.run_command("sudo cp /usr/bin/qemu-arm-static {}".format(
            os.path.join(self.mnt_path, "usr/bin")
        ))
        self.run_command("sudo mount -o bind /dev {}".format(
            os.path.join(self.mnt_path, "dev")
        ))
        self.run_command("sudo mount -o bind /proc {}".format(
            os.path.join(self.mnt_path, "proc")
        ))
        self.run_command("sudo mount -o bind /sys {}".format(
            os.path.join(self.mnt_path, "sys")
        ))

        return True

    def umount(self):
        '''Clean and umounts everything if exist'''

        dev_path = os.path.join(self.mnt_path, "dev")
        self._umount_fs(dev_path)
        proc_path = os.path.join(self.mnt_path, "proc")
        self._umount_fs(proc_path)
        sys_path = os.path.join(self.mnt_path, "sys")
        self._umount_fs(sys_path)
        self._umount_fs(self.mnt_path)

        self.run_command("sudo rm -rf {}".format(self.mnt_path))
        self.run_command("sudo kpartx -dv {}".format(self.img_path))

        return True

    def spawn_chroot(self):
        '''Get user to the chroot shell'''

        if not os.path.ismount(self.mnt_path):
            print('Not mount')
            return

        # self.run_command("sudo chroot {}".format(self.mnt_path))
        subprocess.call(
            "sudo chroot {}".format(self.mnt_path),
            shell=True,
        )

    def run_command(self, command):
        ''''Run specific command on local host machine'''

        subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        )

    def _umount_fs(self, path):
        '''Umount when mounted'''

        if not os.path.ismount(path):
            return

        self.run_command("sudo umount {}".format(
            path
        ))
