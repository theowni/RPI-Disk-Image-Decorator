import subprocess
import os

PATH = os.path.dirname(os.path.realpath(__file__))
MNT_PATH = '/mnt/rpiem'
BOOT_PATH = '/mnt/rpiem-boot'

'''
setup internet below
cp /etc/network/interfaces target/etc/network/interfaces
cp /etc/resolv.conf target/etc/resolv.conf
'''


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
        self.run_command("sudo mkdir -p {}".format(BOOT_PATH))
        self.run_command("sudo mount /dev/mapper/loop0p2 {}".format(
            self.mnt_path))
        self.run_command("sudo mount /dev/mapper/loop0p1 {}".format(
            BOOT_PATH
        ))
        self.run_command("sudo mount -o bind {} {}".format(
            BOOT_PATH,
            os.path.join(self.mnt_path, "boot")
        ))
        self.run_command("sudo cp /usr/bin/qemu-arm-static {}".format(
            os.path.join(self.mnt_path, "usr/bin")
        ))
        self.run_command("sudo mount -t proc /proc {}".format(
            os.path.join(self.mnt_path, "proc")
        ))
        self.run_command("sudo mount -o bind /dev {}".format(
            os.path.join(self.mnt_path, "dev")
        ))
        self.run_command("sudo mount -o bind /dev/pts {}".format(
            os.path.join(self.mnt_path, "dev/pts")
        ))
        self.run_command("sudo mount -o bind /sys {}".format(
            os.path.join(self.mnt_path, "sys")
        ))
        self.run_command_remote("sed -i /.*/s/^/#/ /etc/ld.so.preload")

        return True

    def umount(self):
        '''Clean and umounts everything if exist'''

        self.run_command_remote("sed -i /^#.*/s/^#// /etc/ld.so.preload")
        sys_path = os.path.join(self.mnt_path, "sys")
        self._umount_fs(sys_path)
        proc_path = os.path.join(self.mnt_path, "proc")
        self._umount_fs(proc_path)
        dev_path = os.path.join(self.mnt_path, "dev/pts")
        self._umount_fs(dev_path)
        dev_path = os.path.join(self.mnt_path, "dev")
        self._umount_fs(dev_path)
        boot_path = os.path.join(self.mnt_path, "boot")
        self._umount_fs(boot_path)

        self._umount_fs(BOOT_PATH)
        self._umount_fs(self.mnt_path)

        self.run_command("sudo rm -rf {}".format(BOOT_PATH))
        self.run_command("sudo rm -rf {}".format(self.mnt_path))
        self.run_command("sudo kpartx -dv {}".format(self.img_path))

        return True

    def spawn_chroot(self):
        '''Get user to the chroot shell'''

        if not self.is_mounted():
            print('Not mount')
            return

        # self.run_command("sudo chroot {}".format(self.mnt_path))
        subprocess.call(
            "sudo chroot {} /bin/bash".format(self.mnt_path),
            shell=True,
        )

    def run_command(self, command):
        ''''Run specific command on local host machine'''

        subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        )

    def run_command_remote(self, command):
        '''Run specified command on remote machine'''

        command = "sudo chroot {} /bin/bash -c '{}'".format(
            MNT_PATH,
            command,
        )

        subprocess.call(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        )

    def upload_file(self, file_path, target_path):
        '''Upload file to chroot specified target'''

        if target_path.startswith('/'):
            target_path = target_path[1:]

        self.run_command('sudo cp {} {}'.format(
            file_path,
            os.path.join(MNT_PATH, target_path)
        ))

    def _umount_fs(self, path):
        '''Umount when mounted'''

        if not os.path.ismount(path):
            return

        self.run_command("sudo umount {}".format(
            path
        ))

    def is_mounted(self):
        if not os.path.ismount(self.mnt_path):
            return False

        return True
