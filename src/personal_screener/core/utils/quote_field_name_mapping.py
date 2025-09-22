FIELD_NAME_MAP: dict[str, str] = {}


def get_quote_field_name(template_field_name: str) -> str:
    """
    Map a scoring/filter template field name to a Quote field name.

    Rules:
      1. Check explicit FIELD_NAME_MAP overrides.
      2. Strip 'tiered_' prefix.
      3. Strip '_range' suffix.

    Returns:
        Quote field name, hopefully.
    """
    if template_field_name in FIELD_NAME_MAP:
        return FIELD_NAME_MAP[template_field_name]

    name = template_field_name
    if name.startswith("tiered_"):
        name = name[len("tiered_"):]
    if name.endswith("_range"):
        name = name[: -len("_range")]

    return name
