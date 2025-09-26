import random
import json
import os
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VerseManager:
    """Manages Bible verses with improved selection algorithms."""
    
    def __init__(self, verses_path: str = 'bible_verses.json'):
        self.verses_path = Path(verses_path)
        self._verses: List[Dict[str, Any]] = []
        self.load_verses()
    
    def load_verses(self) -> List[Dict[str, Any]]:
        """Load verses from JSON file with error handling."""
        try:
            if not self.verses_path.is_absolute():
                self.verses_path = Path(__file__).parent / self.verses_path
            
            with open(self.verses_path, 'r', encoding='utf-8') as f:
                self._verses = json.load(f)
            
            logger.info(f"Loaded {len(self._verses)} verses from {self.verses_path}")
            return self._verses
        
        except FileNotFoundError:
            logger.error(f"Verses file not found: {self.verses_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in verses file: {e}")
            return []
    
    def pick_verse(self, topic: Optional[str] = None, keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Pick a verse based on topic or keywords with improved matching.
        
        Args:
            topic: Single topic to match against tags
            keywords: List of keywords to search in tags and text
        
        Returns:
            Dictionary containing verse data
        """
        if not self._verses:
            logger.warning("No verses available")
            return {"ref": "Psalm 23:1", "text": "The LORD is my shepherd; I shall not want.", "tags": ["comfort"]}
        
        candidates = self._verses.copy()
        
        # Filter by topic if provided
        if topic:
            topic_matches = [v for v in candidates if self._matches_topic(v, topic)]
            if topic_matches:
                candidates = topic_matches
        
        # Filter by keywords if provided
        if keywords:
            keyword_matches = [v for v in candidates if self._matches_keywords(v, keywords)]
            if keyword_matches:
                candidates = keyword_matches
        
        return random.choice(candidates)
    
    def _matches_topic(self, verse: Dict[str, Any], topic: str) -> bool:
        """Check if verse matches a specific topic."""
        tags = verse.get('tags', [])
        return topic.lower() in [tag.lower() for tag in tags]
    
    def _matches_keywords(self, verse: Dict[str, Any], keywords: List[str]) -> bool:
        """Check if verse matches any of the provided keywords."""
        tags = verse.get('tags', [])
        text = verse.get('text', '').lower()
        ref = verse.get('ref', '').lower()
        
        search_text = f"{' '.join(tags)} {text} {ref}".lower()
        
        return any(keyword.lower() in search_text for keyword in keywords)
    
    def get_verses_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Get all verses with a specific tag."""
        return [v for v in self._verses if self._matches_topic(v, tag)]
    
    def search_verses(self, query: str) -> List[Dict[str, Any]]:
        """Search verses by text content."""
        query = query.lower()
        return [v for v in self._verses if query in v.get('text', '').lower()]

# Backward compatibility functions
def load_verses(path: str = 'bible_verses.json') -> List[Dict[str, Any]]:
    """Load verses (backward compatibility)."""
    manager = VerseManager(path)
    return manager._verses

def pick_verse(topic: Optional[str] = None, verses: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Pick a verse (backward compatibility)."""
    if verses:
        # Use old logic for backward compatibility
        if topic:
            choices = [v for v in verses if topic.lower() in ','.join(v.get('tags',[])).lower()]
            if choices:
                return random.choice(choices)
        return random.choice(verses)
    
    # Use new manager
    manager = VerseManager()
    return manager.pick_verse(topic=topic)

def extract_keywords_from_input(user_input: str) -> List[str]:
    """Extract potential keywords from user input for better verse matching."""
    # Common emotional/spiritual keywords that might match verse tags
    keyword_map = {
        # Emotional states
        'scared': ['fear', 'courage'],
        'afraid': ['fear', 'courage'],
        'worried': ['anxiety', 'peace'],
        'anxious': ['anxiety', 'peace'],
        'sad': ['comfort', 'sorrow'],
        'depressed': ['comfort', 'hope'],
        'tired': ['rest', 'strength'],
        'exhausted': ['rest', 'strength'],
        'alone': ['presence', 'comfort'],
        'lonely': ['presence', 'comfort'],
        'stuck': ['help', 'strength'],
        'lost': ['guidance', 'help'],
        'overwhelmed': ['peace', 'rest'],
        'stressed': ['peace', 'rest'],
        'discouraged': ['hope', 'strength'],
        'hopeless': ['hope', 'assurance'],
        'weak': ['strength', 'grace'],
        'broken': ['comfort', 'healing'],
        'hurt': ['comfort', 'healing'],
        
        # Programming/work related
        'bug': ['patience', 'strength'],
        'debugging': ['patience', 'wisdom'],
        'error': ['patience', 'help'],
        'failed': ['hope', 'strength'],
        'failure': ['hope', 'strength'],
        'deadline': ['peace', 'strength'],
        'project': ['wisdom', 'strength'],
        'work': ['strength', 'peace'],
        'job': ['strength', 'guidance'],
        'boss': ['patience', 'wisdom'],
        'team': ['patience', 'love'],
        'meeting': ['peace', 'wisdom'],
        
        # Life situations
        'exam': ['peace', 'strength'],
        'test': ['peace', 'strength'],
        'interview': ['courage', 'peace'],
        'family': ['love', 'patience'],
        'relationship': ['love', 'wisdom'],
        'money': ['trust', 'peace'],
        'health': ['healing', 'strength'],
        'future': ['hope', 'trust'],
        'decision': ['wisdom', 'guidance'],
        'change': ['courage', 'trust'],
        
        # Spiritual states
        'doubt': ['assurance', 'trust'],
        'faith': ['assurance', 'strength'],
        'prayer': ['peace', 'guidance'],
        'god': ['presence', 'love'],
        'jesus': ['love', 'grace'],
        'bible': ['wisdom', 'guidance'],
        'church': ['community', 'love'],
        'sin': ['grace', 'forgiveness'],
        'forgiveness': ['grace', 'peace'],
        'guilt': ['grace', 'peace'],
    }
    
    words = user_input.lower().split()
    keywords = []
    
    for word in words:
        # Direct matches
        if word in keyword_map:
            keywords.extend(keyword_map[word])
        
        # Partial matches for common word endings
        for key, values in keyword_map.items():
            if key in word or word in key:
                keywords.extend(values)
                break
    
    return list(set(keywords))  # Remove duplicates
