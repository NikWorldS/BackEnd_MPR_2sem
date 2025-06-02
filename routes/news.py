import json
import os

from flask import jsonify


def init(app):

    @app.route("/api/news_analyze", methods=['GET'])
    def get_news():
        path = 'metals_news.json'
        if not os.path.exists(path):
            return jsonify({'error': 'News file is not exist'}), 404

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
