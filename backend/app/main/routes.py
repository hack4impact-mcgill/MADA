from . import main
from flask import Flask, jsonify


@main.route("/", methods=["GET"])
def index():
    return jsonify(hello="world")
