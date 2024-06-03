import os
import shutil


def copy_files_recursive(source_path, dest_dir_path):
    """
    Recursively copies files from the source directory to the destination directory.

    Args:
        source_path (str): The path to the source directory.
        dest_dir_path (str): The path to the destination directory.

    Returns:
        None

    This function creates the destination directory if it does not exist. It then iterates over the files in the source directory and its subdirectories. For each file, it checks if it is a regular file. If it is, it copies the file to the destination directory. If the file is not a regular file, it recursively calls itself with the file path as the source directory path and the same destination directory path.

    The function prints the source and destination paths for each copied file.

    Example:
        >>> copy_files_recursive("./source", "./destination")
        # Copies all files from the "./source" directory and its subdirectories to the "./destination" directory.
    """
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)