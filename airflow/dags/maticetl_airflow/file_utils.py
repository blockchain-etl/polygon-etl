def read_file(filepath):
    with open(filepath) as file_handle:
        content = file_handle.read()
        return content
