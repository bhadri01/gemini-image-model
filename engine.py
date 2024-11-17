import google.generativeai as genai
import json


api_key = ""
# Configure the generative AI
genai.configure(api_key=api_key)

def extract_text_from_image(image_path):

    myfile = genai.upload_file(image_path)

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [myfile, "\n\n", "Can you find what text is in this image, And the response need to be in json so that we can able to access it easily."],
    )
    response_text = result.text

    # Clean the response string
    if "```json" in response_text:
        # Extract only the JSON portion
        cleaned_response = response_text.split("```json")[1].split("```")[0].strip()
    else:
        cleaned_response = response_text.strip()

    # Parse the cleaned JSON string
    try:
        parsed_json = json.loads(cleaned_response)
        return {"Status": True, "text": parsed_json['text']}
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return {"Status": False, "Message": "Error parsing the JSON response"}

