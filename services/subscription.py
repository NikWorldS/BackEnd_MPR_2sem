import datetime as dt

class _SubscriptionService:

    def subscription(self, email, database):
        with database.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO subscriptions (
                    email,
                    created_at)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    email,
                    dt.datetime.now(dt.timezone.utc)
                )
            )
            database.commit()
        return

    def unsubscription(self, email, database):
        with database.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM subscriptions
                WHERE email=%s
                """,
                (email,)
            )
            database.commit()
        return

subscription_service = _SubscriptionService()
