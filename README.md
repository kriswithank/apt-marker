# apt-marker
Utility for managing improperly marked apt packages

Reads from packages.txt (should have a single package per line) and prompts for if you would like to keep the package as a manual install or if you would like to set it to auto. After running the program, packages that were either passed or not considered are kept in packages.txt. A back-up of packages.txt before running the program is in packages.old.txt. This is still subject to modification.

Currently all packages listed in packages.txt are assumed to be manually installed. This will be addressed soon.

Currently there is no built in way to generate packages.txt, this will be addressed soon, but for the time being you will have to provide your own. For example, to get a list of all manually installed packages, execute the following in this projects, root directory.

    [user@mypc]$ apt-mark showmanual > packages.txt

Requires python 3 to work.

Also on the TODO list is to use the backwards compatible and more stable apt-get and apt-cache commands.
