"""Tests for utility functions."""
import pytest
import json
import tempfile
from pathlib import Path
from utils import VerseManager, extract_keywords_from_input

class TestVerseManager:
    """Test cases for VerseManager class."""
    
    def setup_method(self):
        """Set up test data."""
        self.test_verses = [
            {
                "ref": "Test 1:1",
                "text": "This is a test verse about strength and courage.",
                "tags": ["strength", "courage", "test"]
            },
            {
                "ref": "Test 2:2", 
                "text": "Another test verse about peace and comfort.",
                "tags": ["peace", "comfort", "test"]
            },
            {
                "ref": "Test 3:3",
                "text": "A verse about wisdom and guidance.",
                "tags": ["wisdom", "guidance"]
            }
        ]
    
    def test_verse_manager_initialization(self):
        """Test VerseManager initialization with test data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_verses, f)
            temp_path = f.name
        
        try:
            manager = VerseManager(temp_path)
            assert len(manager._verses) == 3
            assert manager._verses[0]['ref'] == 'Test 1:1'
        finally:
            Path(temp_path).unlink()
    
    def test_pick_verse_by_topic(self):
        """Test verse selection by topic."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_verses, f)
            temp_path = f.name
        
        try:
            manager = VerseManager(temp_path)
            verse = manager.pick_verse(topic='strength')
            assert verse['ref'] == 'Test 1:1'
            assert 'strength' in verse['tags']
        finally:
            Path(temp_path).unlink()
    
    def test_pick_verse_by_keywords(self):
        """Test verse selection by keywords."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_verses, f)
            temp_path = f.name
        
        try:
            manager = VerseManager(temp_path)
            verse = manager.pick_verse(keywords=['peace'])
            assert verse['ref'] == 'Test 2:2'
            assert 'peace' in verse['tags']
        finally:
            Path(temp_path).unlink()
    
    def test_get_verses_by_tag(self):
        """Test getting verses by specific tag."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_verses, f)
            temp_path = f.name
        
        try:
            manager = VerseManager(temp_path)
            test_verses = manager.get_verses_by_tag('test')
            assert len(test_verses) == 2
            
            wisdom_verses = manager.get_verses_by_tag('wisdom')
            assert len(wisdom_verses) == 1
            assert wisdom_verses[0]['ref'] == 'Test 3:3'
        finally:
            Path(temp_path).unlink()

class TestKeywordExtraction:
    """Test cases for keyword extraction."""
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        keywords = extract_keywords_from_input("I'm feeling scared and worried")
        assert 'fear' in keywords
        assert 'courage' in keywords
        assert 'anxiety' in keywords
        assert 'peace' in keywords
    
    def test_extract_keywords_empty(self):
        """Test keyword extraction with no matching words."""
        keywords = extract_keywords_from_input("Hello world")
        assert keywords == []
    
    def test_extract_keywords_multiple(self):
        """Test keyword extraction with multiple matches."""
        keywords = extract_keywords_from_input("I'm tired and overwhelmed")
        assert 'rest' in keywords
        assert 'strength' in keywords
        assert 'peace' in keywords
    
    def test_extract_keywords_case_insensitive(self):
        """Test that keyword extraction is case insensitive."""
        keywords = extract_keywords_from_input("I'm SCARED and Worried")
        assert 'fear' in keywords
        assert 'anxiety' in keywords