"""Provider for Claude Code CLI model - infrastructure only.

This provider is stateless and handles ONLY infrastructure concerns:
- Finding/configuring the CLI binary
- Creating model instances via factory method

Model configuration, tools, and prompts are specified at Agent level.
Provider presets (deepseek, kimi) are part of the model string.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .model import ClaudeCodeModel

logger = logging.getLogger(__name__)


class ClaudeCodeProvider:
    """Provider for Claude Code CLI - infrastructure only.

    This provider is stateless and handles ONLY infrastructure concerns.
    Model configuration, tools, and prompts are specified at Agent level.
    Provider presets are part of the model string.

    Examples:
        >>> provider = ClaudeCodeProvider()
        >>> agent = Agent(model='claude-code:sonnet', ...)  # Uses Anthropic
        >>> agent2 = Agent(model='claude-code:deepseek:sonnet', ...)  # Uses DeepSeek

        # Or create model directly
        >>> model = provider.create_model('sonnet')
        >>> model_with_preset = provider.create_model('sonnet', provider_preset='deepseek')
    """

    def __init__(
        self,
        *,
        cli_path: str | Path | None = None,
    ):
        """Initialize provider with optional CLI path.

        Args:
            cli_path: Path to claude CLI binary. If not provided, searches PATH.
        """
        self._cli_path = str(cli_path) if cli_path else None

        logger.debug(
            "Initialized ClaudeCodeProvider with cli_path=%s",
            self._cli_path,
        )

    @property
    def name(self) -> str:
        """Provider name identifier."""
        return "claude-code"

    @property
    def cli_path(self) -> str | None:
        """Get configured CLI path."""
        return self._cli_path

    def create_model(
        self,
        model_name: str,
        *,
        provider_preset: str | None = None,
    ) -> "ClaudeCodeModel":
        """Create a ClaudeCodeModel instance.

        Called by registration logic when parsing 'claude-code:*' strings.

        Args:
            model_name: Model alias (sonnet, opus, haiku) or full model name
            provider_preset: Optional preset ID (deepseek, kimi, etc.)

        Returns:
            Configured ClaudeCodeModel instance
        """
        # Import here to avoid circular dependency
        from .model import ClaudeCodeModel

        return ClaudeCodeModel(
            model_name=model_name,
            provider_preset=provider_preset,
            cli_path=self._cli_path,
        )

    def __repr__(self) -> str:
        """String representation."""
        return f"ClaudeCodeProvider(cli_path={self._cli_path!r})"
