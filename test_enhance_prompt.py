"""Standalone test script for enhance_prompt.

Usage:
    python test_enhance_prompt.py --base_url <url> --api_key <key> --model <model> --prompt <prompt> [--style <style>] [--max_tokens N] [--temperature F] [--top_p F] [--top_k N]

Examples:
    # Test with OpenAI
    python test_enhance_prompt.py --base_url https://api.openai.com/v1 --api_key sk-xxx --model gpt-4o --prompt "a cat sitting on a table"

    # Test with local Ollama
    python test_enhance_prompt.py --base_url http://localhost:11434/v1 --api_key "" --model llama3 --prompt "a sunset over mountains"

    # Test with specific style and sampling params
    python test_enhance_prompt.py --base_url https://api.openai.com/v1 --api_key sk-xxx --model gpt-4o --prompt "a cat" --style "anime" --temperature 0.5 --top_p 0.8
"""

import argparse
import asyncio
import sys

from prompt_enhancer_llm import PromptEnhancer, STYLE_PROMPTS


class MockClip:
    """Minimal CLIP mock for testing enhance_prompt outside ComfyUI."""

    def tokenize(self, text):
        return {"tokens": text}

    def encode_from_tokens(self, tokens, return_pooled=True):
        cond = {"encoded": tokens}
        pooled = {"pooled": True}
        return cond, pooled


def test_call_openai_compatible(base_url, api_key, model, prompt, style="none", max_tokens=4096, temperature=None, top_p=None, top_k=None):
    """Test the LLM API call directly (no CLIP dependency)."""
    enhancer = PromptEnhancer()

    style_prompt = STYLE_PROMPTS.get(style, "")
    user_content = f"{style_prompt} {prompt}" if style_prompt else prompt

    print("=" * 60)
    print("Direct API Call Test")
    print("=" * 60)
    print(f"  Base URL   : {base_url}")
    print(f"  Model      : {model}")
    print(f"  Style      : {style}")
    print(f"  Input      : {prompt}")
    print(f"  max_tokens : {max_tokens}")
    if temperature: print(f"  temperature: {temperature}")
    if top_p:       print(f"  top_p      : {top_p}")
    if top_k:       print(f"  top_k      : {top_k}")
    if style_prompt:
        print(f"  Style prefix applied: {style_prompt[:80]}...")
    print("-" * 60)

    result = asyncio.run(enhancer._call_openai_compatible(base_url, api_key, model, user_content, max_tokens, temperature, top_p, top_k))

    print(f"  Enhanced output:")
    print(f"    {result}")
    print("=" * 60)
    return result


def test_enhance_prompt(base_url, api_key, model, prompt, style="Basic Styles > none", max_tokens=4096, temperature=None, top_p=None, top_k=None):
    """Test the full enhance_prompt flow with a mock CLIP object."""
    enhancer = PromptEnhancer()
    clip = MockClip()

    if " > " not in style:
        style = f"Basic Styles > {style}"

    print("=" * 60)
    print("Full enhance_prompt Test (with MockClip)")
    print("=" * 60)
    print(f"  Base URL   : {base_url}")
    print(f"  Model      : {model}")
    print(f"  Style      : {style}")
    print(f"  Input      : {prompt}")
    print(f"  max_tokens : {max_tokens}")
    if temperature: print(f"  temperature: {temperature}")
    if top_p:       print(f"  top_p      : {top_p}")
    if top_k:       print(f"  top_k      : {top_k}")
    print("-" * 60)

    conditioning, enhanced = asyncio.run(
        enhancer.enhance_prompt(clip, prompt, base_url, api_key, model, style, max_tokens, temperature, top_p, top_k)
    )

    print(f"  Enhanced prompt:")
    print(f"    {enhanced}")
    print(f"  Conditioning structure: {conditioning}")
    print("=" * 60)
    return enhanced


def main():
    parser = argparse.ArgumentParser(description="Test enhance_prompt with a live LLM endpoint")
    parser.add_argument("--base_url", required=True, help="OpenAI-compatible API base URL")
    parser.add_argument("--api_key", required=True, help="API key (use empty string for local models)")
    parser.add_argument("--model", required=True, help="Model name (e.g. gpt-4o, llama3)")
    parser.add_argument("--prompt", required=True, help="Input prompt to enhance")
    parser.add_argument("--style", default="none", help="Style name (e.g. anime, photorealistic)")
    parser.add_argument("--max_tokens", type=int, default=4096, help="Max tokens (default: 4096)")
    parser.add_argument("--temperature", type=float, default=None, help="Temperature (0.0-2.0, omit for API default)")
    parser.add_argument("--top_p", type=float, default=None, help="Top-p (0.0-1.0, omit for API default)")
    parser.add_argument("--top_k", type=int, default=None, help="Top-k (0-500, omit for API default)")
    parser.add_argument("--full", action="store_true", help="Run full enhance_prompt test (with MockClip)")

    args = parser.parse_args()

    try:
        if args.full:
            test_enhance_prompt(args.base_url, args.api_key, args.model, args.prompt, args.style, args.max_tokens, args.temperature, args.top_p, args.top_k)
        else:
            test_call_openai_compatible(args.base_url, args.api_key, args.model, args.prompt, args.style, args.max_tokens, args.temperature, args.top_p, args.top_k)
    except Exception as e:
        print(f"\n  ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()