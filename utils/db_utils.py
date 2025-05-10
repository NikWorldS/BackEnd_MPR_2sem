def sub_exists(email: str, database) -> bool:
    """
    Checks if user already have subscription.

    :param email: mail of user
    :param database: connection to the database
    :return: True if user already have subscription, False otherwise
    """
    with database.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1 
            FROM subscriptions
            WHERE email=%s
            """,
            (email,)
        )
        result = cursor.fetchone()
        return result is not None
