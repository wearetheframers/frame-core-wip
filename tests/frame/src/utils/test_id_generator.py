import pytest
from frame.src.utils.id_generator import generate_id


def test_generate_id():
    # Test that generate_id returns a string
    assert isinstance(generate_id(), str)

    # Test that generate_id returns a UUID (36 characters long)
    assert len(generate_id()) == 36

    # Test that generate_id returns unique values
    id1 = generate_id()
    id2 = generate_id()
    assert id1 != id2


@pytest.mark.parametrize("num_ids", [10, 100, 1000])
def test_generate_id_uniqueness(num_ids):
    # Test uniqueness for a larger number of generated IDs
    ids = set(generate_id() for _ in range(num_ids))
    assert len(ids) == num_ids


import pytest
from frame.src.utils.id_generator import generate_id


def test_generate_id():
    # Test that generate_id returns a string
    assert isinstance(generate_id(), str)

    # Test that generate_id returns a UUID (36 characters long)
    assert len(generate_id()) == 36

    # Test that generate_id returns unique values
    id1 = generate_id()
    id2 = generate_id()
    assert id1 != id2


@pytest.mark.parametrize("num_ids", [10, 100, 1000])
def test_generate_id_uniqueness(num_ids):
    # Test uniqueness for a larger number of generated IDs
    ids = set(generate_id() for _ in range(num_ids))
    assert len(ids) == num_ids
