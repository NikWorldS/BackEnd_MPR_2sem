from flask import request, jsonify
from services.subscription import subscription_service
from utils.db_utils import sub_exists
import re

def init(app, database):

    @app.route("/api/mail/sub", methods=["POST"])
    def subscription():
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return jsonify({'error': 'Missing required fields'}), 400
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  #Simple mail validator
                return jsonify({'error': 'Invalid email'}), 400
            if sub_exists(email, database):
                return jsonify({'error': 'Email is already subscribed'}), 400

            subscription_service.subscription(email, database)

            return jsonify({'message': 'User subscribed'}), 201
        except Exception as ex:
            print(repr(ex))
            return jsonify({'error': 'Internal server error'}), 500


    @app.route('/api/mail/unsub', methods=['DELETE'])
    def unsubscription():
        try:
            email = request.json['email']

            if not email:
                return jsonify({'error': 'Email is required'}), 400
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  #Simple mail validator
                return jsonify({'error': 'Invalid email'}), 400
            if not sub_exists(email, database):
                return jsonify({'error': 'No such subscription'}), 404

            subscription_service.unsubscription(email, database)

            return jsonify({'message': 'User unsubscribed'}), 200
        except Exception as ex:
            print(repr(ex))
            return jsonify({'error': 'Internal server error'}), 500
