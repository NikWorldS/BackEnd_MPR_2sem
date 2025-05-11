from . import predict, mail


def init(app, database, redis_cache):
    predict.init(app, redis_cache)
    mail.init(app, database)
