from typing import Optional


def validate_word_text(text: str) -> str:
    """Validate word text."""
    if not text or not text.strip():
        raise ValueError("Word text cannot be empty")
    if len(text.strip()) > 256:
        raise ValueError("Word text cannot exceed 256 characters")
    return text.strip()


def validate_quality(quality: int) -> int:
    """Validate review quality score."""
    if quality < 0 or quality > 5:
        raise ValueError("Quality must be between 0 and 5")
    return quality


def validate_optional_text(text: Optional[str], max_length: int = 2048) -> Optional[str]:
    """Validate optional text fields."""
    if text is None:
        return None
    if len(text) > max_length:
        raise ValueError(f"Text cannot exceed {max_length} characters")
    return text