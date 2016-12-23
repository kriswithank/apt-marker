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

KEEP_PKG = 0
REMOVE_PKG = 1
EXIT = 2



def handle_response(term_rdeps):
    while True:
        response = input('Enter a command (h for help): ')

        if response == 'h':
            print(MENU)
        elif response == 's':
            term_show = subprocess.run(['apt-cache', 'show', term_rdeps.args[3]])
        elif response == 'r':
            print(term_rdeps.stdout.decode('utf-8'))
        elif response == 'rr':
            term_recurse_rdeps = subprocess.run(term_rdeps.args + ['--recurse',])
        elif response == 'p':
            return KEEP_PKG
        elif response == 'a':
            term_make_auto = subprocess.run(['sudo', 'apt-mark', 'auto', term_rdeps.args[3]])
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

        term_rdeps = subprocess.run(['apt', 'rdepends', '--installed', line.strip()], stdout=subprocess.PIPE)
        num_lines = term_rdeps.stdout.decode("utf-8").count('\n')

        if num_lines <= 2:
            output_file.write(line)
        else:
            print(term_rdeps.stdout.decode("utf-8"))
            result = handle_response(term_rdeps)

            if result == KEEP_PKG:
                output_file.write(line)
            elif result == EXIT:
                output_file.write(line)
                quit = True

rename(SOURCE_FILE_NAME, OLD_FILE_NAME)
rename(OUTPUT_FILE_NAME, SOURCE_FILE_NAME)
