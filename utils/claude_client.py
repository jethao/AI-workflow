import os
from typing import Optional, Dict, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeClient:
    """Wrapper for Claude API client"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude client

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set in environment or passed to constructor")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using Claude API

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional arguments for Claude API

        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]

        request_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
            **kwargs
        }

        if system_prompt:
            request_params["system"] = system_prompt

        response = self.client.messages.create(**request_params)

        return response.content[0].text

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """
        Generate structured output (JSON) using Claude API

        Args:
            prompt: User prompt
            system_prompt: System prompt
            response_format: Expected response format hints
            **kwargs: Additional arguments

        Returns:
            Generated text (typically JSON)
        """
        enhanced_prompt = prompt
        if response_format:
            enhanced_prompt = f"{prompt}\n\nPlease respond with valid JSON matching this format: {response_format}"

        return self.generate(
            prompt=enhanced_prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for structured output
            **kwargs
        )
