def build_exodus_response(values, index):
    return [{"type": "exodus", "value": float(v), "date": str(d)} for v, d in zip(values, index)]
