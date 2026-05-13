# Changelog

All notable changes to this project will be documented in this file.

## [3.0.0] - 2026-05-13

### Breaking Changes
- **Removed all LLM SDK dependencies** (openai, anthropic, google-generativeai)
  - Now uses only `aiohttp` for async HTTP calls to any OpenAI-compatible endpoint
- **Unified LLM provider** into a single `openai_compatible` option
  - Works with OpenAI, Azure, Ollama, vLLM, LM Studio, LiteLLM, and any OpenAI-compatible API
  - Removed separate provider dropdowns (OpenAI, Anthropic, Google, OpenRouter, Ollama)

### Added
- **Hierarchical style menu** with category dropdown (`style_category`) and dynamic style dropdown
  - Categories: Basic Styles, Fantasy & Horror, Traditional Art, Art Movements, Asian Art Styles, Traditional Media, Digital & Contemporary, Genre & Theme, Decorative Arts
  - JavaScript-powered dynamic style options that update when category changes
- **Configurable API endpoint** (`base_url`) and `model` fields
  - Switch between different LLM backends without code changes
- **Async node execution** — non-blocking LLM calls that won't freeze ComfyUI

### Removed
- `pkg_resources` auto-install logic from `__init__.py`
- All hardcoded LLM provider logic and duplicated code
- Dead JS code that referenced non-existent widgets

### Changed
- Version bumped to 3.0.0
- Updated all dependencies to `aiohttp>=3.9.0`

## [1.1.0] - 2025-01-24

### Added
- OpenRouter support
  - Added OpenRouter client integration
  - Added OpenRouter API key configuration
  - Added OpenRouter as a new LLM provider option
  - Updated documentation with OpenRouter setup instructions
- Improved style selection interface
  - Added category prefixes to styles (e.g., "Basic Styles > detailed")
  - Simplified style selection to a single dropdown
  - Better organization of styles by category

### Fixed
- Added sumi-e style to "Asian Art Styles" category in style selection dropdown
  - Previously defined but not accessible in the UI
  - Now properly categorized with other Asian art styles
- Moved "howls castle" style to "Asian Art Styles" category
  - Better categorization with other Studio Ghibli-related styles
  - Improved style organization and discoverability
- Fixed style selection UI
  - Removed dependency on JavaScript
  - Implemented more reliable Python-based solution
  - Improved user experience with categorized style list

### Changed
- Updated requirements.txt to include openrouter-client
- Improved LLM provider initialization and handling
- Enhanced error handling for API requests
- Enhanced comic book style instructions
  - Added detailed specifications for line art, coloring, and composition
  - Included technical parameters for comic-specific visual elements
  - Improved clarity and effectiveness of the style generation
- Updated default Ollama model to llama3.2:1b
  - Changed from llama2:latest for better performance
  - Optimized for prompt enhancement tasks
- Simplified style selection architecture
  - Removed JavaScript-based implementation
  - Integrated style categories directly into Python code
  - Improved reliability and maintainability

Made with ❤️ by pinkpixel
