import pydantic
import pytest

from mopidy.models import Artist, Chapter


def test_start_is_required_and_frozen():
    chapter = Chapter(start=5000)
    assert chapter.start == 5000
    with pytest.raises(pydantic.ValidationError):
        chapter.start = 1  # models are immutable


def test_optional_fields_default():
    chapter = Chapter(start=0)
    assert chapter.length is None
    assert chapter.name is None
    assert chapter.artists == frozenset()


def test_full_chapter():
    chapter = Chapter(
        start=318000,
        length=402000,
        name="Kerala",
        artists=frozenset([Artist(name="Bonobo")]),
    )
    assert chapter.name == "Kerala"
    assert {a.name for a in chapter.artists} == {"Bonobo"}
    assert chapter.length == 402000


def test_serialises_with_model_tag():
    data = Chapter(start=0, name="Intro").model_dump(by_alias=True)
    assert data["__model__"] == "Chapter"
    assert data["start"] == 0
    assert data["name"] == "Intro"
