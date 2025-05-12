def get_kunde_by_key(api_key: str, kunden: dict):
    for kunde, info in kunden.items():
        if info["api_key"] == api_key:
            return kunde, info
    return None, None

