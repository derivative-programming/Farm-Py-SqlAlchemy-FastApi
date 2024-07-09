# services/custom_temp_folder.py  # pylint: disable=duplicate-code # noqa: E501
"""
A class that creates a custom temporary folder and
provides methods to create temporary files and clear
the folder.
"""
import tempfile
import os
import shutil


class CustomTempFolder:
    """
    A class that creates a custom temporary folder and
    provides methods to create temporary files and clear
    the folder.
    """
    def __init__(self, subfolder_name='my_custom_subfolder'):
        self.default_temp_dir = tempfile.gettempdir()
        self.custom_temp_subdir = os.path.join(
            self.default_temp_dir, subfolder_name)
        os.makedirs(self.custom_temp_subdir, exist_ok=True)

    def create_temp_file(self, prefix='tmp', suffix='.txt'):
        """
        Creates a temporary file in the custom temporary folder.
        """
        temp_file = tempfile.NamedTemporaryFile(
            dir=self.custom_temp_subdir,
            prefix=prefix,
            suffix=suffix,
            delete=False)
        print(f'Temporary file created at: {temp_file.name}')
        return temp_file

    def clear_temp_folder(self):
        """
        Clears all files and directories in the custom
        temporary folder.
        """
        count = 0
        for filename in os.listdir(self.custom_temp_subdir):
            file_path = os.path.join(self.custom_temp_subdir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    # Delete the file or symbolic link
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    # Delete the directory and its contents
                    shutil.rmtree(file_path)
                count += 1
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        print(f'Removing temp files...count: {count}')

        print("All files and directories in"
              f" {self.custom_temp_subdir} have been cleared.")
