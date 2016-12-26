from os import rename
import subprocess



SOURCE_FILE_NAME = 'packages.txt'
OUTPUT_FILE_NAME = 'packages.results.txt'
OLD_FILE_NAME = 'packages.old.txt'

MENU = """  s -> apt show package
  p -> pass on package (do nothing)
  h -> help
  a -> sudo apt-make auto package
  c -> confirm manual
  q -> quit
  r -> apt rdepends --installed
  rr -> apt rdepends --installed --recurse"""

# TODO: move these to PackageMinipulator.
KEEP_PKG = 0
REMOVE_PKG = 1
EXIT = 2



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class PackageMinipulator:
    def __init__(self, name):
        self.name = name
        self.rdeps = None
        self.rrdeps = None
        self.show = None


    def has_rdeps(self):
        if self.rdeps == None:
            print('first time has_rdeps')
            self.get_rdeps()

        return self.rdeps.stdout.decode('utf-8').count('\n') > 2

    def get_show_info(self):
        if self.show == None:
            print('first time get_show_info')
            self.show = subprocess.run(['apt-cache', 'show', self.name], stdout=subprocess.PIPE)

        return self.show.stdout.decode('utf-8')


    def mark_auto(self):
        term_auto = subprocess.run(['sudo', 'apt-mark', 'auto', self.name], stdout=subprocess.PIPE)

        return term_auto.stdout.decode('utf-8')

    def get_rdeps(self):
        if self.rdeps == None:
            print('first time get_rdeps')
            self.rdeps = subprocess.run(['apt', 'rdepends', '--installed', self.name], stdout=subprocess.PIPE)

        return self.rdeps.stdout.decode('utf-8')


    def get_rrdeps(self):
        if self.rrdeps == None:
            print('first time get_rrdeps')
            self.rrdeps = subprocess.run(['apt', 'rdepends', '--installed', '--recurse', self.name],  stdout=subprocess.PIPE)

        return self.rrdeps.stdout.decode('utf-8')



def handle_response(pkg):
    while True:
        response = input(bcolors.BOLD + 'Enter a command (h for help): ' + bcolors.ENDC)

        if response == 'h':
            print(MENU)
        elif response == 's':
            print(pkg.get_show_info())
        elif response == 'r':
            print(pkg.get_rdeps())
        elif response == 'rr':
            print(pkg.get_rrdeps())
        elif response == 'p':
            return KEEP_PKG
        elif response == 'a':
            print(pkg.mark_auto())
            return REMOVE_PKG
        elif response == 'c':
            return REMOVE_PKG
        elif response == 'q':
            return EXIT
        else:
            print("Invalid response")


quit = False
with open(SOURCE_FILE_NAME) as source_file, open(OUTPUT_FILE_NAME, 'w+') as output_file:
    for line in source_file:

        if quit:
            output_file.write(line)
            continue

        pkg = PackageMinipulator(line.strip())

        if pkg.has_rdeps():
            print(pkg.get_rdeps())
            result = handle_response(pkg)

            if result == KEEP_PKG:
                output_file.write(line)
            elif result == EXIT:
                output_file.write(line)
                quit = True
        else:
            output_file.write(line)

rename(SOURCE_FILE_NAME, OLD_FILE_NAME)
rename(OUTPUT_FILE_NAME, SOURCE_FILE_NAME)
