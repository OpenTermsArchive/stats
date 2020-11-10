from pathlib import Path
import pytest
from lib.cgus import CGUsDataset, CGU

# test CGUsDataset
def test_path_check_ok():
    cgudataset = CGUsDataset(root_path="tests/data/")
    assert True

def test_path_check_not_a_directory():
    with pytest.raises(AssertionError, match = "is not a directory"):
        cgudataset = CGUsDataset(root_path="tests/data/Instagram/Community Guidelines.md")

def test_path_check_directory_doesnt_exist():
    with pytest.raises(AssertionError, match = "does not exist"):
        cgudataset = CGUsDataset(root_path="tests/wrong_dir/")

def test_list_files():
    cgudataset = CGUsDataset(root_path="tests/data/")
    assert len(list(cgudataset.yield_all_md())) == 6
    assert len(list(cgudataset.yield_all_md(ignore_rootdir=False))) == 7

# test CGU object
def test_CGU_init():
    cgu = CGU(path = Path("tests/data/FakeService/Community Guidelines.md"))
    assert cgu.service == "FakeService"
    assert cgu.document_type == "Community Guidelines"
    assert cgu.name == "Community Guidelines"
    assert cgu.fullname == "FakeService - Community Guidelines"
    assert len(cgu) == 29 # number of words
    assert cgu.sentence_count == 4
    assert cgu.syllable_count == 37

def test_CGU_readability():
    cgu = CGU(path = Path("tests/data/FakeService/Community Guidelines.md"))
    assert round(cgu.readability, 1) == 91.5
    assert round(cgu.readability_grade_level, 1) == 2.3

def test_CGU_dict():
    EXPECTED_KEYS = {"document_type", "num_words", "readability", "readability_grade_level"}
    cgu = CGU(path = Path("tests/data/FakeService/Community Guidelines.md"))
    outdict = cgu.to_dict()
    assert isinstance(outdict, dict)
    assert EXPECTED_KEYS.issubset(outdict.keys())
