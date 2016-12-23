import subprocess



KEEP_PKG = 0
REMOVE_PKG = 1
EXIT = False



def handle_response(term_deps):
    while True:
        response = input('Enter a command (h for help): ')
        
        if response == 'h':
            print("s -> apt show package\np -> pass on package (do nothing)\nh -> help\na -> sudo apt-make auto package\nc -> confirm manual\nq -> quit\nr -> apt rdepends --installed")
        elif response == 's':
            term_show = subprocess.run(['apt', 'show', term_deps.args[3]])
        elif response == 'r':
            print(term_deps.stdout.decode('utf-8'))
        elif response == 'p':
            return KEEP_PKG
        elif response == 'a':
            term_make_auto = subprocess.run(['sudo', 'apt-mark', 'auto', term_deps.args[3]])
            return REMOVE_PKG
        elif response == 'c':
            return REMOVE_PKG
        elif response == 'q':
            global EXIT
            EXIT = True
            return KEEP_PKG
        else:
            print("Invalid response")
    
    

with open('packages.txt') as source_file, open('packages.result.txt', 'w+') as output_file:
    for line in source_file:
        
        if EXIT:
            output_file.write(line)
            continue
    
        term_deps = subprocess.run(['apt', 'rdepends', '--installed', line.strip()], stdout=subprocess.PIPE)
        num_lines = term_deps.stdout.decode("utf-8").count('\n')
        
        if num_lines <= 2:
            output_file.write(line)
        else:
            print(term_deps.stdout.decode("utf-8"))
           
            if handle_response(term_deps) == KEEP_PKG:
                output_file.write(line)
                