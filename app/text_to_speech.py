# t2s1.py
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# Set up the device (use CUDA if available)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

def load_tts_model():
    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")
    return model, tokenizer

def text_to_speech(model, tokenizer, prompt, description, output_path="output_audio.wav"):
    # Tokenize description and prompt
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    
    # Generate audio data
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # Save audio to a WAV file
    sf.write(output_path, audio_arr, model.config.sampling_rate, format='WAV')
    print(f"Audio saved to {output_path}")
    
    return output_path
