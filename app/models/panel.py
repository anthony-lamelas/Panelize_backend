from pydantic import BaseModel, Field, field_validator
from typing import Optional


class PanelRequest(BaseModel):
    """Request model for generating comic panels"""
    story_description: str = Field(..., min_length=1, description="The story to convert into panels")
    num_panels: int = Field(default=1, ge=1, le=10, description="Number of panels to generate")
    style: str = Field(default="manga", description="Visual style/theme for the panels")

    @field_validator('story_description')
    @classmethod
    def validate_story_description(cls, v: str) -> str:
        """Ensure story description is not empty after stripping"""
        if not v.strip():
            raise ValueError("Story description cannot be empty")
        return v.strip()

    @field_validator('style')
    @classmethod
    def validate_style(cls, v: str) -> str:
        """Clean and validate style input"""
        import re
        # Allow only letters, numbers, spaces, and dashes
        sanitized = re.sub(r"[^a-zA-Z0-9\- ]", "", v).strip()
        return sanitized if sanitized else "manga"


class Panel(BaseModel):
    """Individual panel response"""
    prompt: str = Field(..., description="The prompt used to generate this panel")
    image_url: Optional[str] = Field(None, description="URL of the generated image")
    caption: Optional[str] = Field(None, description="AI-generated caption describing the image")


class PanelResponse(BaseModel):
    """Response model for panel generation"""
    panels: list[Panel] = Field(..., description="List of generated panels")
