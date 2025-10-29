from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..models.panel import PanelRequest, PanelResponse
from ..services.openai_service import OpenAIService

panel_bp = Blueprint("panel_bp", __name__)
openai_service = OpenAIService()


@panel_bp.route('/generate-panels', methods=['POST'])
def generate_panels_route():
    """Generate comic panels from a story description"""
    try:
        # Parse and validate request using Pydantic
        data = request.get_json()
        panel_request = PanelRequest(**data)
        
        # Call service to generate panels
        panels = openai_service.generate_panels(
            story_description=panel_request.story_description,
            num_panels=panel_request.num_panels,
            theme=panel_request.style
        )
        
        # Build and validate response
        response = PanelResponse(panels=panels)
        return jsonify(response.model_dump()), 200
    
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    
    except Exception as e:
        print(f"Backend Error: {e}")
        return jsonify({"error": str(e)}), 500

