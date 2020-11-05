import json
import logging
from pathlib import Path, PosixPath

import nltk

logging.basicConfig(level=logging.INFO)


class CGUsDataset():
    """
    Helper class for handling CGUs Versions
    """

    def __init__(self, root_path: str = "../CGUs-versions"):
        self.root_path = Path(root_path)
        assert self.root_path.exists(), f"{root_path} does not exist"
        assert self.root_path.is_dir(), f"{root_path} is not a directory"


    def yield_all_md(self, ignore_rootdir: bool = True) -> list:
        if ignore_rootdir:
            return self.root_path.glob('**/*/*.md')
        else:
            return self.root_path.glob('**/*.md')

class CGU():
    """
    A CGU object, and the main building bloc for our algorithms.
    """

    # Remove all punctuation when tokenizing text
    _TOKENIZER = nltk.tokenize.RegexpTokenizer(r'\w+')

    def __init__(self, path: PosixPath):
        self._path = path
        self.name = self._path.name.removesuffix(".md")
        self.service = self._path.as_posix().split("/")[-2]
        self.fullname = f"{self.service} - {self.name}"
        self.document_type = f"{self.name}"
        self.raw_content = self._path.read_text()
        self.tokens = self._TOKENIZER.tokenize(self.raw_content)


    def to_dict(self) -> dict:
        """
            "Serialize" the CGU object to key/value pairs.
        """
        return {
            "document_type": self.document_type,
            "num_words": len(self)
        }

    def most_used_words(self, n: int = 10):
        return nltk.FreqDist(self.tokens).most_common(n)

    def __str__(self):
        return f"\n{self.fullname}\nLength: {len(self)}\n{self.raw_content[:500]}"

    def __len__(self):
        """Length of a CGU is its number of words/tokens."""
        return len(self.tokens)