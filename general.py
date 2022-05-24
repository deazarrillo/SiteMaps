import os


# Each website crawled is saved to a separate folder
def create_project_dir(directory):
    if not os.path.exists(directory):
        print(f'Creating project {directory}')
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = f'{project_name}/queue.txt'
    crawled = f'{project_name}/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Creates a new file and writing data
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# adding data onto an existing file

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')
        # \n adds a new line so each link is on a new line


# Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass


# Read a file and convert each line to set items
def file_to_set(file_name):
    # type: (object) -> object
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
            # the above code with .replace removes new line character that we added when creating the files
    return results


# Iterate through a set, each item in the set will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file)
    # links is new stuff, file is old stuff therefor we want to delete old stuff
    for link in sorted(links):
        append_to_file(file, link)
