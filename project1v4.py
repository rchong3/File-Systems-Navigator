# Richard Chong
# Brandon Takaki

from pathlib import Path

def get_directory() -> (str, Path):
    '''Takes input from user and returns path for directory.'''
    
    while True:
        user: str = input()
        user = user.split()
        
        if len(user) > 1 and (user[0] == 'D' or user[0] == 'R'):
            path = Path(' '.join(user[1:]))
            if path.is_dir():
                return (user[0], path)
            else:
                print('ERROR')
        else:
            print('ERROR')

def get_files(path: Path, recursive: bool) -> [Path]:
    '''Returns all files under given directory.
    If recursive is true, then include files in subdirectories.'''
    
    files: [Path] = []

    for location in path.iterdir():
        if location.is_file():
            files.append(location)
        elif (recursive and location.is_dir()):
            files += get_files(location, True)
    
    return files

def print_files(files: [Path]) -> None:
    '''Prints all paths in list of file paths.'''
    
    for file in files:
        print(file)
    
def search_characteristics(files: [Path]) -> [Path]:
    '''Narrows the search of files based on certain characteristics.'''
    
    while True:
        user: str = input()
        user = user.split()
        
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
    
    interesting_files = []
    for file in files:
        if name == file.name:
            interesting_files.append(file)
    return interesting_files

def search_extensions(extension: str, files: [Path]) -> [Path]:
    '''Searchs for and returns files of a specific extention.'''
    
    interesting_files = []
    for file in files:
        if extension == file.suffix or '.' + extension == file.suffix:
            interesting_files.append(file)
    return interesting_files
        
def compare_byte(sign: str, value: int, files: [Path]) -> [Path]:
    '''Compares the byte values of files to either greater than or less
        than a certain value, and files that qualify are returned.'''
    
    interesting_files = []
    for path in files:
        file = path.open('rb')
        sum = 0
        for line in file:
            sum += len(line)
        if (sign == '<' and sum < value) or (sign == '>' and sum > value):
            interesting_files.append(path)
    return interesting_files

def search_text(text: str, files: [Path]) -> [Path]:
    '''Searches and returns files that contain a specific text.'''
    interesting_files = []
    for file in files:
        with file.open(mode = 'r') as f:
            for line in f:
                if text in line:
                    interesting_files.append(file)
                    break
    return interesting_files

def use_files(interesting_files: [Path]) -> None:
    valid_input = False
    while valid_input == False:
        valid_input = True
        user: str = input()
        user = user.split()
        
        if user[0] == "F":
            print_first_lines(interesting_files)
        elif user[0] == "D":
            duplicate_files(interesting_files)
        elif user[0] == "T":
            touch_files(interesting_files)
        else:
            valid_input = False

def print_first_lines(interesting_files: [Path]) -> None:
    for path in interesting_files:
        try:
            file = path.open(mode = 'r')
            print(file.readline())
            file.close()
        except:
            print('NOT TEXT')

def duplicate_files(interesting_files: [Path]) -> None:
    for path in interesting_files:
        duplicate = Path(str(path) + '.dup')
        duplicate.write_bytes(path.read_bytes())

def touch_files(interesting_files: [Path]) -> None:
    for path in interesting_files:
        path.touch()


if __name__ == '__main__':
    user, path = get_directory()
    files: [Path] = get_files(path, user == 'R')
    files.sort()
    print_files(files)
    interesting_files = search_characteristics(files)
    print_files(interesting_files)
    if len(interesting_files) > 0:
        use_files(interesting_files)
