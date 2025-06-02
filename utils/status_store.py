def is_training(redis_client, model_key):
    return redis_client.get(f'model_status:{model_key}') == b'training'

def set_training_status(redis_client, model_key):
    redis_client.set(f"model_status:{model_key}", "training", ex=3600)  # expire через час

def clear_status(redis_client, model_key):
    redis_client.delete(f"model_status:{model_key}")