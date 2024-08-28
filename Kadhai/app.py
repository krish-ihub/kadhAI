from flask import Flask, request, jsonify, send_file, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
import os

app = Flask(__name__)

# Initialize APIs
elevenlabs_api_key = "sk_ae96ec6c20655f44f98654cf91425de9142f2c5044917cfd"
elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)

# Initialize Tamillama model
tokenizer = AutoTokenizer.from_pretrained("RajuKandasamy/tamillama_tiny_30m")
model = AutoModelForCausalLM.from_pretrained("RajuKandasamy/tamillama_tiny_30m")

def generate_tamil_story(prompt: str) -> str:
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    generation_output = model.generate(input_ids=input_ids, max_new_tokens=256)
    generated_text = tokenizer.decode(generation_output[0])

    # Remove unwanted parts and extract Tamil story
    start_index = generated_text.find("கதை:")
    end_index = generated_text.find("English Translation:")
    
    if start_index == -1:
        return "Error: Tamil story part not found"
    
    tamil_story = generated_text[start_index:end_index].strip() if end_index != -1 else generated_text[start_index:].strip()
    
    return tamil_story

def text_to_speech_file(text: str) -> str:
    output_directory = "audio_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    response = elevenlabs_client.text_to_speech.convert(
        voice_id="gCr8TeSJgJaeaIoV4RWH",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    save_file_path = os.path.join(output_directory, f"{uuid.uuid4()}.mp3")
    print(f"Saving file to: {save_file_path}")

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    return save_file_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_prompt = data.get('prompt')

    if not user_prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    # Generate Tamil story
    tamil_story = generate_tamil_story(user_prompt)
    
    # Convert Tamil story to speech
    audio_file = text_to_speech_file(tamil_story)

    response = {
        'story': tamil_story,
        'audio': os.path.basename(audio_file)  # Return only the file name
    }

    return jsonify(response)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join("audio_files", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)  # Set as_attachment=False to stream the file
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
