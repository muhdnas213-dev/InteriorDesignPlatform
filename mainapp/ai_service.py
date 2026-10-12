import os
import json
import base64
import mimetypes

from google import genai


def analyze_room_with_gemini(image_path):

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    # Read image
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    # Detect image type
    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "image/jpeg"

    # Convert image to base64
    image_data = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are an AI interior design assistant for DesignNest.

Analyze this interior room image.

Identify:

1. Room type
2. Main furniture items
3. Dominant colors
4. Interior design style
5. Lighting type
6. Flooring type if visible
7. Wall characteristics if visible
8. Interior design suggestions

Return ONLY valid JSON using exactly this structure:

{
    "room_type": "",
    "furniture": [],
    "colors": [],
    "style": "",
    "lighting": "",
    "flooring": "",
    "walls": "",
    "suggestions": []
}
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image",
                "data": image_data,
                "mime_type": mime_type
            }
        ]
    )

    text = interaction.output_text.strip()

    # Remove Markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)