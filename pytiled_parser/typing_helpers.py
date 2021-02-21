def is_float(string: str):
    try:
        float(string)
        return True
    except (ValueError, TypeError):
        return False
