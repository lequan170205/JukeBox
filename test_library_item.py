import pytest
from library_item import LibraryItem  # Assuming the class is in library_item.py

@pytest.fixture
def sample_item():
    """Fixture to create a sample LibraryItem object."""
    return LibraryItem(name="Song Title", artist="Artist Name", rating=3)

def test_initialization(sample_item):
    """Test the initialization of LibraryItem."""
    assert sample_item.name == "Song Title"
    assert sample_item.artist == "Artist Name"
    assert sample_item.rating == 3
    assert sample_item.play_count == 0

def test_info(sample_item):
    """Test the info method."""
    expected_info = "Song Title - Artist Name ***"
    assert sample_item.info() == expected_info

def test_stars(sample_item):
    """Test the stars method."""
    assert sample_item.stars() == "***"

def test_play_count(sample_item):
    """Test updating the play count."""
    sample_item.play_count += 1
    assert sample_item.play_count == 1
