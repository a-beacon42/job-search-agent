import textwrap


def truncate(text: str, max_chars: int = 260) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    # wrap to avoid cutting mid-word
    wrapped = textwrap.shorten(text, width=max_chars, placeholder="…")
    return wrapped
