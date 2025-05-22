from flask import Blueprint, request, jsonify
from ..services.openai_service import generate_panels

panel_bp = Blueprint("panel_bp", __name__)

@panel_bp.route('/generate-panels', methods=['POST', 'GET', 'OPTIONS'])
def generate_panels_route():
    data = request.get_json()
    story_description = data.get('story_description', "")
    num_panels = data.get('num_panels', 1)
    theme = data.get('style', 'manga')

    # Validate inputs, if invalid return error
    if not story_description or num_panels < 1:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        # Call service function (openai_service.py) to generate panels
        results = generate_panels(story_description, num_panels, theme)
        return jsonify({"panels": results}), 200
    
    except Exception as e:
        print("Backend Error:", e)
        return jsonify({"error": str(e)}), 500

