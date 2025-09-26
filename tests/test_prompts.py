"""Tests for prompt templates."""
import pytest
from prompts import BIBLE_MOTIVATE_PROMPT, PROGRAMMER_MOTIVATE_PROMPT, get_prompt_for_context

class TestPrompts:
    """Test cases for prompt templates."""
    
    def test_bible_motivate_prompt_variables(self):
        """Test that the Bible motivate prompt has correct input variables."""
        expected_vars = ['user_input', 'verse_ref', 'verse_text']
        assert BIBLE_MOTIVATE_PROMPT.input_variables == expected_vars
    
    def test_programmer_motivate_prompt_variables(self):
        """Test that the programmer motivate prompt has correct input variables."""
        expected_vars = ['user_input', 'verse_ref', 'verse_text']
        assert PROGRAMMER_MOTIVATE_PROMPT.input_variables == expected_vars
    
    def test_bible_motivate_prompt_format(self):
        """Test formatting the Bible motivate prompt."""
        formatted = BIBLE_MOTIVATE_PROMPT.format(
            user_input="I'm feeling sad",
            verse_ref="Psalm 23:1",
            verse_text="The LORD is my shepherd; I shall not want."
        )
        
        assert "I'm feeling sad" in formatted
        assert "Psalm 23:1" in formatted
        assert "The LORD is my shepherd" in formatted
    
    def test_programmer_motivate_prompt_format(self):
        """Test formatting the programmer motivate prompt."""
        formatted = PROGRAMMER_MOTIVATE_PROMPT.format(
            user_input="I'm stuck on a bug",
            verse_ref="Joshua 1:9",
            verse_text="Be strong and of a good courage"
        )
        
        assert "I'm stuck on a bug" in formatted
        assert "Joshua 1:9" in formatted
        assert "Be strong and of a good courage" in formatted
    
    def test_get_prompt_for_context_general(self):
        """Test getting prompt for general context."""
        prompt = get_prompt_for_context("general")
        assert prompt == BIBLE_MOTIVATE_PROMPT
    
    def test_get_prompt_for_context_programmer(self):
        """Test getting prompt for programmer context."""
        prompt = get_prompt_for_context("programmer")
        assert prompt == PROGRAMMER_MOTIVATE_PROMPT
    
    def test_get_prompt_for_context_default(self):
        """Test getting prompt for unknown context defaults to general."""
        prompt = get_prompt_for_context("unknown")
        assert prompt == BIBLE_MOTIVATE_PROMPT