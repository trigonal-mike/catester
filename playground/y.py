def get_item(haystack: list[tuple[str, object]], needle, default):
    for x, y in enumerate(haystack):
        s, o = y
        if s == needle:
            return o
    return default

