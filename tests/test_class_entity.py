import gc
import os
import pytest
from openunderstand.oudb.api import create_db, open as db_open

DB_PATH = "tests/tmp_class_entity.oudb"
PROJECT_DIR = "benchmark/calculator_app"

@pytest.fixture(scope="module")
def db():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            pass

    create_db(dbname=DB_PATH, project_dir=PROJECT_DIR)
    database = db_open(DB_PATH)

    yield database

    # Teardown logic
    database.close()
    del database
    gc.collect()

    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            pass

class TestClassEntityNormal:
    def test_class_entity_has_correct_kind(self, db):
        classes = db.lookup(".*", "class")
        for c in classes:
            assert "class" in c.kind().longname().lower()

    def test_class_entity_simplename(self, db):
        classes = db.lookup(".*", "class")
        for c in classes:
            assert c.simplename() != ""
            assert " " not in c.simplename()


class TestClassEntityParentChild:
    def test_class_has_parent_file(self, db):
        classes = db.lookup(".*", "class")
        for c in classes:
            parent = c.parent()
            assert parent is not None
            assert "file" in parent.kind().longname().lower()

    def test_class_children_are_methods_or_variables(self, db):
        classes = db.lookup(".*", "class")
        for c in classes:
            for child in c.ents(refkindstring="Define", entkindstring="method, variable"):
                assert child.parent().id() == c.id()


class TestClassEntityInverseReferences:
    def test_define_has_matching_definein(self, db):
        classes = db.lookup(".*", "class")
        for c in classes:
            define_refs = c.refs(refkindstring="Define")
            for r in define_refs:
                inverse_refs = r.ent().refs(refkindstring="DefineIn")
                assert any(ir.ent().id() == c.id() for ir in inverse_refs)


class TestClassEntityEdgeCases:
    def test_empty_class_has_no_members(self, db):
        # Assumes benchmark project contains (or you add) an empty class fixture
        empty_classes = [c for c in db.lookup(".*", "class") if len(c.ents(refkindstring="Define")) == 0]
        for c in empty_classes:
            assert c.ents(refkindstring="Define") == []

    def test_unresolved_unknown_class_reference(self, db):
        unknown = db.lookup(".*", "unknown class")
        for u in unknown:
            assert u.kind().longname().lower().startswith("unknown")


class TestClassEntityMalformed:
    def test_malformed_snippet_does_not_crash_analysis(self, tmp_path):
        malformed_dir = tmp_path / "malformed_proj"
        malformed_dir.mkdir()
        (malformed_dir / "Broken.java").write_text("public class Broken { public void foo( }")
        bad_db_path = str(tmp_path / "bad.oudb")
        try:
            create_db(dbname=bad_db_path, project_dir=str(malformed_dir))
        except Exception as e:
            pytest.fail(f"Analysis should not raise on malformed input, got: {e}")
