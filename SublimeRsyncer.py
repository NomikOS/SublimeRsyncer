import sublime
import sublime_plugin
import subprocess
import sys


class SublimeRsyncer(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        # sublime.status_message("wwwww")
        settings = sublime.load_settings('SublimeRsyncer.sublime-settings')
        folders = settings.get("folders")
        current_file = view.file_name()
        if folders:
            for folder in folders:
                if current_file[:len(folder['localPath'])] == folder['localPath']:
                    # spawn a thread so non-blocking
                    thread = Rsync(folder['localPath'], folder['remote'], folder['exclude'], folder['deleteAfter'])
                    thread.run() #.start()


class Rsync(object): #threading.Thread):
    def __init__(self, localPath, remote, exclude, deleteAfter):
        self.localPath = localPath
        self.remote = remote
        self.exclude = exclude
        self.deleteAfter = deleteAfter
        self.result = None

    def run(self):

        commandComponents = ['rsync', '-avz', self.localPath, self.remote]

        if self.deleteAfter:
            commandComponents.insert(2, "--delete-after")

        if self.exclude:
            for excludeItem in self.exclude:
                commandComponents.insert(2, "--exclude="+excludeItem)

        sys.stdout.write('SublimeRsyncer command: '+' '.join(commandComponents)+'\n');
        sys.stdout.flush()

        process = subprocess.Popen(
            commandComponents,
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
