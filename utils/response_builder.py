def build_response(data_type, values, index) -> list:
    return [{"type": data_type, "value": float(v), "date": str(d)} for v, d in zip(values, index)]
