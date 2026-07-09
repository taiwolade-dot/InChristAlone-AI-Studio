def format_citation(style, source_type, fields):
    if style == "apa7":
        return _format_apa7(source_type, fields)
    elif style == "turabian":
        return _format_turabian(source_type, fields)
    return "Unsupported citation style."


def _format_apa7(source_type, fields):
    author = fields.get("author", "").strip()
    year = fields.get("year", "").strip()
    title = fields.get("title", "").strip()
    source = fields.get("source", "").strip()
    volume = fields.get("volume", "").strip()
    pages = fields.get("pages", "").strip()
    url = fields.get("url", "").strip()

    if source_type == "book":
        citation = f"{author} ({year}). {title}. {source}."
    elif source_type == "journal":
        vol_part = f", {volume}" if volume else ""
        pages_part = f", {pages}" if pages else ""
        citation = f"{author} ({year}). {title}. {source}{vol_part}{pages_part}."
    elif source_type == "website":
        citation = f"{author} ({year}). {title}. {source}. {url}"
    else:
        citation = f"{author} ({year}). {title}."

    return citation.strip()


def _format_turabian(source_type, fields):
    author = fields.get("author", "").strip()
    year = fields.get("year", "").strip()
    title = fields.get("title", "").strip()
    source = fields.get("source", "").strip()
    place = fields.get("place", "").strip()
    pages = fields.get("pages", "").strip()
    url = fields.get("url", "").strip()

    if source_type == "book":
        place_part = f"{place}: " if place else ""
        citation = f'{author}. {title}. {place_part}{source}, {year}.'
    elif source_type == "journal":
        pages_part = f": {pages}" if pages else ""
        citation = f'{author}. "{title}." {source} ({year}){pages_part}.'
    elif source_type == "website":
        citation = f'{author}. "{title}." {source}. Accessed {year}. {url}.'
    else:
        citation = f"{author}. {title}. {year}."

    return citation.strip()


SOURCE_TYPE_FIELDS = {
    "book": ["author", "year", "title", "source", "place"],
    "journal": ["author", "year", "title", "source", "volume", "pages"],
    "website": ["author", "year", "title", "source", "url"],
}

SOURCE_TYPE_LABELS = {
    "book": "Book",
    "journal": "Journal Article",
    "website": "Website",
}