# Brandon Takaki 18956857
# Richard Chong 85923095

from pathlib import Path

def get_directory() -> (str, Path):
    '''Takes input from user and returns path for directory.'''
    valid_input = False
    while not valid_input:
        user: str = input()
        user: [str] = user.split()
        
        if len(user) == 2 and (user[0] == 'D' or user[0] == 'R'):
            path = Path(' '.join(user[1:]))
            if path.is_dir():
                valid_input = True
            else:
                print('ERROR') 
        else:
            print('ERROR')
    return (user[0], path)

def get_files(path: Path, recursive: bool) -> [Path]:
    '''Returns all files under given directory.
    If recursive is true, then include files in subdirectories.'''
    
    files: [Path] = []
    directories: [Path] = []

    try:
        for location in path.iterdir():
            if location.is_file():
                files.append(location)
            elif (recursive and location.is_dir()):
                directories.append(location)
    finally:
        files.sort()
        directories.sort()

        for directory in directories:
            files += get_files(directory, True)
        
        return files

def print_files(files: [Path]) -> None:
    '''Prints all paths in list of file paths.'''
    
    for file in files:
        print(file)
    
def search_characteristics(files: [Path]) -> [Path]:
    '''Narrows the search of files based on certain characteristics.'''
    
    while True:
        user: str = input()
        user: [str] = user.split()
        
        if len(user) == 1 and user[0] == 'A':
            return files
        elif len(user) >= 2:
            if user[0] == 'N':
                return search_name(' '.join(user[1:]), files)
            elif user[0] == 'E':
                return search_extensions(' '.join(user[1:]), files)
            elif user[0] == 'T':
                return search_text(' '.join(user[1:]), files)
            elif (user[0] == '<' or user[0] == '>') and user[1].isnumeric():
                return compare_byte(user[0], int(user[1]), files)
            else:
                print('ERROR')
        else:
            print('ERROR')

def search_name(name: str, files: [Path]) -> [Path]:
    '''Searchs for and returns files of a specific name.'''
    
    interesting_files: [Path] = []
    for file in files:
        if name == file.name:
            interesting_files.append(file)
    return interesting_files

def search_extensions(extension: str, files: [Path]) -> [Path]:
    '''Searchs for and returns files of a specific extention.'''
    
    interesting_files: [Path] = []
    for file in files:
        if extension == file.suffix or '.' + extension == file.suffix:
            interesting_files.append(file)
    return interesting_files
        
def compare_byte(sign: str, value: int, files: [Path]) -> [Path]:
    '''Compares the byte values of files to either greater than or less
        than a certain value, and files that qualify are returned.'''
    
    interesting_files: [Path] = []
    for file in files:
        size = len(file.read_bytes())
        if (sign == '<' and size < value) or (sign == '>' and size > value):
            interesting_files.append(file)
    return interesting_files

def search_text(text: str, files: [Path]) -> [Path]:
    '''Searches and returns files that contain a specific text.'''
    interesting_files: [Path] = []
    for file in files:
        with file.open(mode = 'r') as f:
            try:
                for line in f:
                    if text in line:
                        interesting_files.append(file)
                        break
            except:
                continue
    return interesting_files

def take_action(files: [Path]) -> None:
    '''Take the third input from the user to take action on the
        interesting files.'''
    while True:
        user: str = input()
        if user == 'F':
            return print_1st_lines(files)
        elif user == 'D':
            return make_duplicates(files)
        elif user == 'T':
            return touch_files(files)
        else:
            print('ERROR')

def print_1st_lines(files: [Path]) -> None:
    '''Print the first line of all the interesting files.'''
    for path in files:
        try:
            file = path.open('r')
            line = file.readline()
            if line[-1] == '\n':
                print(line[:-1])
            else:
                print(line)
            file.close()
        except:
            print('NOT TEXT')

def make_duplicates(files: [Path]) -> None:
    '''Create duplicates of all the interesting files.'''
    for path in files:
        p = Path(str(path) + '.dup')
        p.write_bytes(path.read_bytes())

def touch_files(files: [Path]) -> None:
    '''Change all the interesting files so they have the current date
        and time.'''
    for path in files:
        path.touch()

if __name__ == '__main__':
    user, path = get_directory()
    files: [Path] = get_files(path, user == 'R')
    print_files(files)
    interesting_files = search_characteristics(files)
    print_files(interesting_files)
    if not (interesting_files == []):
        take_action(interesting_files)
