from functools import partial
from enum import Enum
from os import rename
import subprocess



SOURCE_FILE_NAME = 'packages.txt'
OUTPUT_FILE_NAME = 'packages.results.txt'
OLD_FILE_NAME = 'packages.old.txt'



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class PkgMinipultor:

    class Status(Enum):
        UNDECIDED = 0
        KEEP = 1
        REMOVE = 2

    def __init__(self, name):
        self.name = name
        self.rdeps = None
        self.rrdeps = None
        self.show = None
        self.status = PkgMinipultor.Status.UNDECIDED


    def has_rdeps(self):
        if self.rdeps == None:
            self.get_rdeps()

        return self.rdeps.stdout.decode('utf-8').count('\n') > 2

    def get_show_info(self):
        if self.show == None:
            self.show = subprocess.run(['apt-cache', 'show', self.name], stdout=subprocess.PIPE)

        return self.show.stdout.decode('utf-8')


    def mark_auto(self):
        term_auto = subprocess.run(['sudo', 'apt-mark', 'auto', self.name], stdout=subprocess.PIPE)
        self.mark_remove()
        return term_auto.stdout.decode('utf-8')


    def mark_keep(self):
        self.status = PkgMinipultor.Status.KEEP


    def mark_remove(self):
        self.status = PkgMinipultor.Status.REMOVE


    def get_rdeps(self):
        if self.rdeps == None:
            self.rdeps = subprocess.run(['apt', 'rdepends', '--installed', self.name], stdout=subprocess.PIPE)

        return self.rdeps.stdout.decode('utf-8')


    def get_rrdeps(self):
        if self.rrdeps == None:
            self.rrdeps = subprocess.run(['apt', 'rdepends', '--installed', '--recurse', self.name],  stdout=subprocess.PIPE)

        return self.rrdeps.stdout.decode('utf-8')



class Menu:

    def __init__(self):
        self.quit = False

    def __str__(self):
        return ("  s -> apt show package\n"
                "  p -> pass on package (do nothing)\n"
                "  h -> help\n"
                "  a -> sudo apt-make auto package\n"
                "  c -> confirm manual\n"
                "  q -> quit\n"
                "  r -> apt rdepends --installed\n"
                "  rr -> apt rdepends --installed --recurse\n")


    def handle_response(self, pkg):

        def respond_quit():
            self.quit = True

        responses = {
            'h': partial(print, str(self)),
            's': partial(print, pkg.get_show_info()),
            'r': partial(print, pkg.get_rdeps()),
            'rr': partial(print, pkg.get_rrdeps()),
            'p': pkg.mark_keep,
            'a': lambda: pkg.mark_auto(),   # Needed for lazy evaluation. Yay Python!...
            'c': pkg.mark_remove,
            'q': respond_quit,
        }

        while (not self.quit) and pkg.status == PkgMinipultor.Status.UNDECIDED:
            response = input(bcolors.BOLD + 'Enter a command (h for help): ' + bcolors.ENDC)

            try:
                responses[response]()
            except:
                print('Invalid response')



with open(SOURCE_FILE_NAME) as source_file, open(OUTPUT_FILE_NAME, 'w+') as output_file:
    menu = Menu()
    for line in source_file:

        pkg = PkgMinipultor(line.strip())

        if (not menu.quit) and pkg.has_rdeps():
            print(pkg.get_rdeps())
            menu.handle_response(pkg)

            if pkg.status == PkgMinipultor.Status.REMOVE:
                continue    # Do not write pkg to output_file.

        output_file.write(line)

rename(SOURCE_FILE_NAME, OLD_FILE_NAME)
rename(OUTPUT_FILE_NAME, SOURCE_FILE_NAME)
