import sublime
import sublime_plugin
import subprocess
import sys
from functools import reduce


class SublimeRsyncer(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        # sublime.status_message("wwwww")
        settings = sublime.load_settings('SublimeRsyncer.sublime-settings')
        folders = settings.get("folders")
        current_file = view.file_name()
        if folders:
            for folder in folders:
                if folder.get('active') and current_file[:len(folder['localPath'])] == folder['localPath']:
                    # spawn a thread so non-blocking
                    thread = Rsync(
                        folder['localPath'],
                        folder['remote'],
                        folder['exclude'],
                        delete_after = folder.get('deleteAfter'),
                        ssh_port = folder.get('ssh_port'),
                        ssh_config = folder.get('ssh_config'),
                        ssh_identity_file= folder.get('ssh_identity_file'),
                    )
                    thread.run()


class Rsync(object):

    def __init__(self, localPath, remote, exclude,
                 delete_after=False, ssh_port=None, ssh_config=None, ssh_identity_file=None):
        self.localPath = localPath
        self.remote = remote
        self.exclude = exclude
        self.delete_after = delete_after
        self.result = None
        self.e_ssh = reduce(lambda a,b: True if (a or b) else False, [
            ssh_port,
            ssh_config,
            ssh_identity_file
        ], None)
        self.ssh_port = ssh_port
        self.ssh_config = ssh_config
        self.ssh_identity_file = ssh_identity_file

    def run(self):
        command_components = ['rsync', '-avzl']

        e_ssh = []
        if self.e_ssh:
            if self.ssh_port:
                e_ssh.append(['-p', self.ssh_port])
            if self.ssh_config:
                e_ssh.append(['-F', self.ssh_config])
            if self.ssh_identity_file:
                e_ssh.append(['-i', self.ssh_identity_file])
            if len(e_ssh) > 0:
                e_ssh = reduce(
                    lambda a,b: "{li} {k} '{v}' ".format(li=a,k=b[0],v=b[1]),
                    e_ssh,
                    'ssh '
                )
                command_components.extend(['-e', "\"{cmd}\"".format(cmd=e_ssh)])

        if self.delete_after:
            command_components.insert(2, "--delete-after")

        if self.exclude:
            for exclude_item in self.exclude:
                command_components.insert(2, "--exclude="+exclude_item)

        command_components.extend([self.localPath, self.remote])
        sys.stdout.write('SublimeRsyncer command: '+' '.join(command_components)+'\n')
        sys.stdout.flush()

        process = subprocess.Popen(
            command_components,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        rc = process.wait()

        if rc != 0:
            print("SublimeRsyncer: Failed, rc={}".format(rc))
        else:
            print("SublimeRsyncer: Done.")

        return
