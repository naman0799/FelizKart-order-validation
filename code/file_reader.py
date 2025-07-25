
def read_files(filepath):
    """ Reads a CSV file from the given path and returns all data rows excluding the header. """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            return lines[1:]  # skip header
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []
