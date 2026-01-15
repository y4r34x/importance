"""Text processing utilities."""
import re


def clean_text(text: str) -> str:
    """
    Clean up text by normalizing whitespace and removing artifacts.

    Args:
        text: Raw text content

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Replace non-breaking spaces and other unicode spaces
    text = text.replace('\xa0', ' ')
    text = text.replace('\u00a0', ' ')

    # Remove HTML comment artifacts (Field: Page, Field: Sequence, etc.)
    text = re.sub(r'Field:\s*/?(?:Page|Sequence|/Page|/Sequence)[^F]*?(?=Field:|$)', '', text)
    text = re.sub(r'Field:\s*\S+[^F]*', '', text)

    # Remove standalone page numbers at end of text (e.g., " 2" or " 3")
    text = re.sub(r'\s+\d{1,2}\s*$', '', text)

    # Normalize multiple spaces to single space
    text = re.sub(r' +', ' ', text)

    # Normalize multiple newlines to double newline (paragraph break)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove empty lines at start/end
    text = text.strip()

    return text
