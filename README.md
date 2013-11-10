# Sublime Rsyncer
Forked from Jimmy Forrester (http://github.com/jimmysparkle/SublimeRsyncer). Jimmy, thanks!

A Sublime Text 3 plugin which allows you to rsync specific folders on save. Please note this requires you to have setup an SSH key with a blank password to allow this to rsync without requiring a password. Please see section of this document titled SSH Keys

## Installation

Download (or clone) the latest source from [GitHub](http://github.com/xenolog/SublimeRsyncer) into your Sublime Text "Packages" directory.

The "Packages" directory is located at:

* OS X:
  ~/Library/Application Support/Sublime Text 3/Packages/

* Linux:
  ~/.config/sublime-text-3/Packages/

* Windows:
  %APPDATA%/Sublime Text 3/Packages/

!!! Do not put package to User directory !!!

## Usage

Edit your user settings Preferences -> Package Settings -> SublimtRsyncer -> Settings - User

An example config could look like so:

```
{
  "folders": [
    {
      "localPath" : "/Users/jimmy/code/project1/",
      "remote"  : "jimmy@my-vm:/var/www/project1/",
      "exclude" : [".git", ".svn"],
      "ssh_port"   : "2222",
      "ssh_config" : "/tmp/ssh_config",
      "ssh_identity_file" : "/tmp/ssh_identity_file",
      "deleteAfter" : true
    },
    {
      "localPath" : "/Users/jimmy/code/project2/",
      "remote"  : "jimmy@192.168.0.55:/var/www/project2/",
      "exclude" : [".git", ".svn"],
      "deleteAfter" : false
    }
  ]
}
```

Be carefylly with slash ('/') at end of both paths.

When you next save a file using Sublime Text 3 it will itterate through the folders you've specified and if it matches the file saved it will attempt to rsync. The output can be monitored in the Sublime Text 2 console.

## SSH Keys

You need to generate an SSH key on the machine that you're using Sublime Text 3 on, you should create this with a blank password. You then need to add the public key to your remote machines .ssh/authorized_keys file. You need to make sure that the authorized_keys file has the correct permissions set.

chmod 400 .ssh/authorized_keys