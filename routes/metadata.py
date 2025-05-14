import json

from flask import jsonify


def init(app):
    def load_metadata():
        with open('metadata.json', 'r', encoding="UTF-8") as file:
            return json.load(file)

    @app.route('/api/metadata', methods=['GET'])
    def get_metadata():
        metadata = load_metadata()
        return jsonify(metadata)


