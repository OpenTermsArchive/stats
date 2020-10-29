import json
from pathlib import Path, PosixPath

from nltk import word_tokenize

class CGUsDataset():
    """
    Helper class for handling CGUs Versions
    """

    def __init__(self, root_path: str = "../CGUs-versions"):
        self.root_path = Path(root_path)
        assert self.root_path.exists(), f"{root_path} does not exist"
        assert self.root_path.is_dir(), f"{root_path} is not a directory"


    def _yield_all_md(self, ignore_rootdir: bool = True) -> list:
        if ignore_rootdir:
            return self.root_path.glob('**/*/*.md')
        else:
            return self.root_path.glob('**/*.md')

class CGU():
    """
    A CGU object, and the main building bloc for our algorithms.
    """

    def __init__(self, path: PosixPath):
        self._path = path
        self.name = self._path.name
        self.source = self._path.as_posix().split("/")[-2]
        self.fullname = f"{self.source} - {self.name}"
        self.cgu_type = "TODO" #TODO add CGU type
        self.raw_content = self._path.read_text()
        self.parsed_content = word_tokenize(self.raw_content)


    def to_dict(self, json: bool = False):
        """
            Serialize the CGU object to key/value pairs.
            Returns a dict object by default.
            If `json`, returns a json string.
        """
        return {
            "full_name": self.fullname,
            "cgu_type": self.cgu_type,
            "raw_content": self.raw_content
        }

    def __str__(self):
        return f"\n{self.fullname}\nLength: {len(self)}\n{self.raw_content[:500]}"

    def __len__(self):
        """Length of a CGU is its number of words."""
        return len(self.parsed_content)


if __name__ == "__main__":
    p = Path("../CGUs-versions/Google Ads/Trackers Policy.md")
    cgu = CGU(p)
    print(cgu.to_dict())
    print(len(cgu))