# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:02:20 2025

@author: Shubham Mohindru
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from parser import parse_decision_tree, compute_ev, ParseError

app = Flask(__name__)
CORS(app)

@app.route('/parse', methods=['POST'])
def parse():
    data = request.get_json(force=True)
    text = data.get('text', '')
    try:
        tree = parse_decision_tree(text)
        tree = compute_ev(tree)
        return jsonify({'status': 'success', 'tree': tree})
    except ParseError as pe:
        return jsonify({'status': 'error', 'message': str(pe)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)