import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('prompt_enhancer')

try:
    # Try relative import first
    try:
        from .prompt_enhancer_llm import PromptEnhancer
    except ImportError:
        # If that failed, try direct import
        from prompt_enhancer_llm import PromptEnhancer

    logger.info("Successfully imported PromptEnhancer class")

    NODE_CLASS_MAPPINGS = {
        "PromptEnhancer": PromptEnhancer
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "PromptEnhancer": "Prompt Enhancer LLM ✨"
    }

    WEB_DIRECTORY = "./js"

    __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

    logger.info("Node registration complete")

except Exception as e:
    logger.error(f"Error during node initialization: {e}")
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
