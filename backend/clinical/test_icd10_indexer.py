import pytest
from clinical.services.icd10_indexer import ICD10HierarchyIndexer

def test_icd10_indexer():
    res = ICD10HierarchyIndexer.get_chapter("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
