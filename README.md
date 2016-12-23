# apt-marker
Utility for managing improperly marked apt packages

Reads from packages.txt (should have a single package per line) and prompts for if you would like to keep the package as a manual install or if you would like to set it to auto. The files that were either passed or not considered are currently being put into packages.result.txt. This will be changed soon.

Currently all packages listed in packages.txt are assumed to be manually installed. This will be addressed soon.

Currently there is no built in way to generate packages.txt, this will be addressed soon, but for the time being you will have to provide your own. For example, to get a list of all manually installed packages, execute the following in this projects, root directory.

    [user@mypc]$ apt-mark showmanual > packages.txt

Requires python3 to work.

Also on the TODO list is to use the backwards compatible and more stable apt-get and
apt-cache commands.
