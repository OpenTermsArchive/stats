from datetime import datetime
import json
import logging
from pathlib import Path, PosixPath

import nltk

logging.basicConfig(level=logging.INFO)

# download CMU pronunciation data to compute number of syllables
try:
    nltk.data.find('corpora/cmudict')
except LookupError:
    logging.info("Downloading cmudict pronunciation data (this should happen just once, next runs will be faster)")
    nltk.download('cmudict')

# download punkt for sentence tokenizer
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.info("Downloading punkt tokenizer (this should happen just once, next runs will be faster)")
    nltk.download('punkt')

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
    A CGU object, and the main building block for our algorithms.
        The `is_historical` argument allows for parsing a historical CGUs-versions
        dataset which has a slightly different naming convention.
    """

    # Remove all punctuation when tokenizing text
    _TOKENIZER = nltk.tokenize.RegexpTokenizer(r'[a-zA-Z0-9]+')

    # Carnegie Mellon University (CMU) pronunciation data
    _PRONDICT = nltk.corpus.cmudict.dict()

    def __init__(self, path: PosixPath, is_historical: bool = False):
        self._path = path
        self.is_historical = is_historical
        # parse info from file path differently depending on the mode
        if self.is_historical:
            self.version_date = datetime.fromisoformat(self._path.name.removesuffix(".md"))
            self.name = self._path.as_posix().split("/")[-2]
            self.service = self._path.as_posix().split("/")[-3]
            self.fullname = f"{self.service} - {self.name} - {self.version_date}"
        else:
            self.name = self._path.name.removesuffix(".md")
            self.service = self._path.as_posix().split("/")[-2]
            self.fullname = f"{self.service} - {self.name}"
        
        self.document_type = f"{self.name}"
        self.raw_content = self._path.read_text()
        self.tokens = [token.lower() for token in self._TOKENIZER.tokenize(self.raw_content)]
        # these are useful for computing readability measures
        self.sentence_count = len(nltk.tokenize.sent_tokenize(self.raw_content))
        self.syllable_count = sum([self._num_syllables(token) for token in self.tokens])
        # readability measures
        #https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
        self.readability = 206.835 - 1.015 * (len(self) / self.sentence_count) - 84.6 * (self.syllable_count / len(self))
        self.readability_grade_level = 0.39 * (len(self) / self.sentence_count) + 11.8 * (self.syllable_count / len(self)) - 15.59


    def to_dict(self) -> dict:
        """
            "Serialize" the CGU object to key/value pairs.
        """
        return {
            "document_type": self.document_type,
            "num_words": len(self),
            "readability": self.readability,
            "readability_grade_level": self.readability_grade_level
        }

    def __str__(self):
        return f"\n{self.fullname}\nIs Historical Data: {self.is_historical}\nLength: {len(self)}\n\n{self.raw_content[:500]} ..."

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        """Length of a CGU is its number of words/tokens."""
        return len(self.tokens)

    
    def _num_syllables(self, word):
        """
            Count the number of syllables in a word using CMU's pronunciation dictionary
        """

        # in the CMU dictionnary, vowels end with a digit e.g. 'AH0'
        def _vowels_count(pronunciation):
            return len([phoneme_code for phoneme_code in pronunciation if phoneme_code[-1].isdigit()])
        
        cmu_pronunciation = self._PRONDICT.get(word)
        
        # if word not in cmu dictionary -> 1
        if cmu_pronunciation is None:
            return 1

        # if more than one pronunciation, take the longest
        return max(map(_vowels_count, cmu_pronunciation))