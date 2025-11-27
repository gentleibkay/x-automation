def get_trends():
    """
    Temporary fallback trend generator.
    Worker needs this to function.
    Replace later with real Google/Reddit/API integrations.
    """

    return [
        {"title": "Tech Meme Viral", "tagline": "meme"},
        {"title": "New Music Drop", "tagline": "entertainment"},
        {"title": "Football Transfer Alert", "tagline": "sports"},
        {"title": "Breaking News", "tagline": "global update"},
    ]
