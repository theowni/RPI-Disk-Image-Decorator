import subprocess
import os

PATH = os.path.dirname(os.path.realpath(__file__))
MNT_PATH = '/tmp/rpiem'


class EmulateManager:
    mounted = False

    def __init__(self, img_path, mnt_path=MNT_PATH):
        self.img_path = img_path
        self.mnt_path = mnt_path

    def mount_image(self):
        '''Setup mounting point and prepare filesystems'''

        self.run_command("sudo kpartx -av {}".format(self.img_path))
        self.run_command("sudo mkdir {}".format(self.mnt_path))
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

        self.mounted = True
        return True

    def clean(self):
        '''Clean and umounts everything'''
        self.run_command("sudo umount {}".format(
            os.path.join(self.mnt_path, "dev")
        ))
        self.run_command("sudo umount {}".format(
            os.path.join(self.mnt_path, "proc")
        ))
        self.run_command("sudo umount {}".format(
            os.path.join(self.mnt_path, "sys")
        ))
        self.run_command("sudo umount {}".format(self.mnt_path))
        self.run_command("sudo rm -rf /mnt/rpiem")
        self.run_command("sudo kpartx -dv {}".format(self.img_path))

        self.mounted = False
        return True

    def spawn_chroot(self, command):
        if not self.mounted:
            raise Exception('Image is not mounted, mount it first!')

        self.run_command("sudo chroot {}".format(self.mnt_path))

    def run_command(self, command):
        subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        )
