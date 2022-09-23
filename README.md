# vimwiki\_recent

Read your vimwiki files sorted by last used and create a list

- Author: Tuncay D.
- Source: https://github.com/thingsiplay/vimwiki\_recent
- License: [MIT License](LICENSE)

## What is this?

**vimwiki_recent** is simply a "script" to generate a list of recently used
vimwiki files for Vim. That's the entire job of it.
[VimWiki](https://github.com/vimwiki/vimwiki) is a plugin for
[Vim](https://vimdoc.sourceforge.net).

## How to use

### Installation

This script is written in Python and therefore requires Python 3 to be
installed. Download the script, give it the executable bit and put it in a
folder that is in the "PATH". It does not read other files than the vimwiki
folder you point to and does not create other files than the "recent.wiki"
file. Here is a simple instruction you can follow (you don't have to):

    git clone https://github.com/thingsiplay/vimwiki_recent
    cd vimwiki_recent
    chmod +x vimwiki_recent.py
    install -m 755 vimwiki_recent.py "$(systemd-path user-binaries)/vimwiki_recent"

To uninstall from that location, just delete the script or use following
command (provided you installed it with the above command without altering it):

    rm -f "$(systemd-path user-binaries)/vimwiki_recent"

Notice how I removed the file extension ".py" when installing the script. The
following examples assumes you removed the extension too, but that is
absolutely an optional step and just my personal preference.

### General functionality

Just run the script from commandline with pointing to the root directory of
your vimwiki folder. At default it will create or update a file named
"recent.wiki" in that folder, containing a list of files as wiki links.  At the
moment only the Vimwiki syntax language is supported. You can also output the
content of the file that would be written to the stdout without changing the
file. Here is an example command:

    vimwiki_recent -d ~/vimwiki -Xo

Omit the option `-X` and the default file will be created at
"~/vimwiki/recent.wiki". Use the `--help` option to list all available options.

### Automation

Now you want probably not run this command everytime yourself when it is
needed. Therefore add a few auto commands to your vimrc. Here is a suggestion:

    # Always save automatically a wiki entry when leaving buffer.
    :au BufLeave *.wiki w

    # Use command to create and update the recent file through a script.
    :au BufCreate,BufEnter recent.wiki silent ! vimwiki_recent -d ~/vimwiki

Now each time you visit a .wiki file in your vimwiki, its modification time
will be changed when you leave the buffer. The other command will run the
script to update the "recent.wiki" file each time just before you open the
"recent.wiki" file. It's content lists all last edited or visited files in
order as a typical wiki link.

### Add the file to your overview

The last thing you need to do is actually linking the file at
"~/vimwiki/recent.wiki" as a link to your overview page at
"~/vimwiki/index.wiki". And I suggest to add it at the top, so each time you
open your index page, the most recent files will be available at your
fingertips.

At that point you don't need to do anything else ever again. The script should
run automatically each time when needed and provide you the latest edited wiki
entries.
