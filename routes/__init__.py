from . import predict, mail


def init(app, database):
    predict.init(app, database)
    mail.init(app, database)
