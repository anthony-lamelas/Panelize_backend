import openai
import os
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration # type: ignore
import torch
from io import BytesIO
from PIL import Image
from typing import Optional
from ..models.panel import Panel


class OpenAIService:
    """Service for generating comic panels using OpenAI and BLIP"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._blip_processor: Optional[BlipProcessor] = None
        self._blip_model: Optional[BlipForConditionalGeneration] = None
        self._device: Optional[str] = None
    
    def generate_panels(self, story_description: str, num_panels: int, theme: str) -> list[Panel]:
        """Generate comic panels from a story description"""
        
        # Step 1: Use GPT to break down the story into panel prompts
        panel_prompts = self._generate_panel_prompts(story_description, num_panels, theme)
        
        # Step 2: Generate images for each prompt
        panels = self._generate_images(panel_prompts)
        
        return panels
    
    def _generate_panel_prompts(self, story_description: str, num_panels: int, theme: str) -> list[str]:
        """Use GPT to break down a story into individual panel prompts"""
        system_msg = (
            f"You are a prompt engineer for DALL·E. "
            f"Take the user's story and split it into multiple panel prompts, create the story in the theme provided. "
            f"Each panel describes a distinct scene in detail, in under 1000 characters each. Make sure to include nothing violent (that DALLE won't generate) "
            f"'In colored {theme} theme generate the following:' "
            f"in the beggining of each prompt. "
            f"Return them as a numbered list, for example:\n"
            f"Panel 1: This is the theme {theme}. In color, generate the following: <prompt text>\n"
            f"Panel 2: This is the theme {theme}. In color, generate the following: <prompt text>\n"
            f"..."
        )
        
        user_msg = f"Break this story into {num_panels} prompts:\n\n{story_description}"
        
        gpt_response = self.client.chat.completions.create(  
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ]
        )
        
        content = gpt_response.choices[0].message.content
        if not content:
            raise ValueError("GPT returned empty content.")
        
        return self._parse_gpt_panels(content, num_panels)
    
    def _parse_gpt_panels(self, gpt_content: str, num_panels: int) -> list[str]:
        """Parse GPT output into individual panel prompts"""
        lines = gpt_content.strip().split("\n")
        panel_prompts = []
        current_prompt = []
        
        for line in lines:
            if "Panel" in line and ":" in line:
                # If we have an existing prompt, finalize it
                if current_prompt:
                    panel_prompts.append("\n".join(current_prompt).strip())
                    current_prompt = []
                
                # Start a new prompt
                current_prompt.append(line.split(":", 1)[1].strip())
            else:
                current_prompt.append(line.strip())
        
        # Add last prompt
        if current_prompt:
            panel_prompts.append("\n".join(current_prompt).strip())
        
        return panel_prompts[:num_panels]
    
    def _generate_images(self, panel_prompts: list[str]) -> list[Panel]:
        """Generate DALL-E images for each panel prompt"""
        panels = []
        previous_caption = ""
        
        for i, panel_prompt in enumerate(panel_prompts):
            # For the first panel, use the original prompt
            if i == 0:
                used_prompt = panel_prompt
            else:
                # For subsequent panels, combine the previous caption + new prompt
                used_prompt = (
                    "Generate this next image based on the following description "
                    f"of the previous image as you are telling a story: {previous_caption}. {panel_prompt}"
                )
            
            print(f"[DEBUG] Generating image for prompt: '{used_prompt}'")
            
            try:
                image_response = self.client.images.generate(
                    prompt=used_prompt,
                    n=1,
                    size="1024x1024",
                    model="dall-e-3"
                )
                
                print(f"[DEBUG] Image response: {image_response}")
                
                if not image_response.data or not image_response.data[0].url:
                    panels.append(Panel(prompt=used_prompt, image_url=None, caption=None))
                    continue
                
                image_url = image_response.data[0].url
                
                # Caption using BLIP
                caption = None
                if image_url:
                    image_bytes = requests.get(image_url).content
                    caption = self._caption_image(image_bytes)
                
                previous_caption = caption if caption else ""
                panels.append(Panel(prompt=used_prompt, image_url=image_url, caption=caption))
                
            except Exception as e:
                print(f"[ERROR] Failed to generate image: {e}")
                panels.append(Panel(prompt=used_prompt, image_url=None, caption=None))
        
        return panels
    
    def _caption_image(self, image_bytes: bytes) -> str:
        """Generate a caption for an image using BLIP model"""
        # Lazy-load and cache BLIP processor/model
        if self._blip_processor is None or self._blip_model is None or self._device is None:
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            self._blip_processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base", 
                use_fast=True
            )
            self._blip_model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            self._blip_model.to(self._device)  # type: ignore
        
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess & generate caption
        inputs = self._blip_processor(img, return_tensors="pt")  # type: ignore
        inputs = {k: v.to(self._device) for k, v in inputs.items()}
        
        with torch.no_grad():
            output_ids = self._blip_model.generate(
                **inputs,
                max_length=300,
                num_beams=7,
                do_sample=True,
                top_k=100,
                top_p=0.95,
                temperature=1.2,
                early_stopping=False
            )
        
        # Decode the output tokens 
        caption = self._blip_processor.decode(output_ids[0], skip_special_tokens=True)  # type: ignore
        return caption
