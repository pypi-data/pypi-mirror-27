import os
import platform

# TODO: Add increment version option to the user interface.
# TODO: Add logging of successfully build versions.


class Versioner(object):
    """Helper class allowing easy version number changes when building apps."""

    def __init__(self, root="", file=""):
        """Initialize object.

        Args:
            root (str): Project's root directory for the search (can be
                relative or absolute).
            file (str): File with the version number.
        """
        self.root = root
        self.file = file
        self._true_path = ""
        """Confirmed path to the version file."""
        self._ver_num = ""
        """Version number obtained from the version file."""

    def _search_file(self):
        """Attempts to find version file from path given in file or
        combination of root/file. If not possible will search for it
        recursively starting at the root.

        Returns:
            (str) | (None): String representing a valid path to the
            version file or None if not found.
        """
        # Sanity checks here.
        if not os.path.isdir(self.root):
            raise NotADirectoryError("Project's root must be a valid directory.")

        path = os.path.join(self.root, self.file)
        top_dir = self.root

        # Confirm if file is a valid path to the version file.
        if os.path.isfile(self.file):

            return self.file

        # Or confirm if root/file is a valid path to the version file.
        elif os.path.isfile(path):

            return path

        # Otherwise search for it.
        else:
            for cur_root, dirs, files in os.walk(top_dir):
                for file in files:
                    if file == self.file:

                        return os.path.join(cur_root, file)

        # If not found return None.
        return None

    @staticmethod
    def _read_file(path):
        """Reads first line of the file containing version number.

        Args:
            path (str): Path to the file with the version number.

        Returns:
            ver_num (str):  Version number.

        """
        try:
            with open(path) as file:
                ver_num = file.read()

            return ver_num

        except IOError as info:
            print("IO Error, ({0}): {1}".format(info.errno, info.strerror))

    def get_version(self, root="../", file="VERSION.txt", prompt=True):
        """Obtains version number from a file.

        Args:
            root (str): Project's root directory for the search (can be
                relative or absolute) Assumption is that build script
                is run from a subfoler of the project's root.
            file (str): File with the version number. Can be just the name
                or relative / absolute path.
            prompt (bool): Check if user interaction should be enabled
                at initial stage of getting version number.

        Returns:
            ver_num (str): Version number.
        """
        self.root = os.path.abspath(root)
        self.file = file

        result = self._search_file()
        if result is None:
            raise ValueError(
                "Version file missing, please check parameters / folders.")
        else:
            self._true_path = result

        self._ver_num = self._read_file(self._true_path)

        if prompt:
            if self.user():
                return self._ver_num
            else:
                raise SystemExit("Version number not accepted. User abort")

        return self._ver_num

    def user(self):
        """Allows interaction with the user.

        Returns:
            (bool): Confirmation from the user if the version number
                found is correct.

        """
        if platform.system() == "Windows":
            command = "cls"
        else:
            command = "clear"
        while True:
            os.system(command)
            print("Path to your version file:\n{0}".format(self._true_path))
            print(
                "Version number in the file is: {0}".format(
                    self._ver_num))
            response = input(
                "Do you want to accept this version number? (y/n)").lower()
            if response not in ["y", "n"]:
                continue
            elif response.lower() == "y":
                return True
            else:
                return False

