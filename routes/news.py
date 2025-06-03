from flask import jsonify
import json
import os

def init(app):

    @app.route("/api/news_analyze", methods=["GET"])
    def get_news():
        path = "metals_news.json"
        if not os.path.exists(path):
            return jsonify({'error': "News file is not exist"}), 404

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
