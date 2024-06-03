import os

def filename_format(filename):
    try:
        # Extract only the file name
        base_filename = os.path.basename(filename)
        # Convert to new file name format
        new_filename = f"datalogszip{base_filename}"
    except Exception as e:
        print(f"Error occurs in filename_formatter:{e}")
    return new_filename