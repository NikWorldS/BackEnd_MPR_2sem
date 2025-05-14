from . import predict, mail, metadata


def init(app, database, redis_cache):
    predict.init(app, redis_cache)
    mail.init(app, database)
    metadata.init(app)
