import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def determine_max_tokens(length):
    if length == "short":
        return 64
    elif length == "medium":
        return 128
    elif length == "long":
        return 256
    else:
        raise ValueError("Invalid length. Please choose 'short', 'medium', or 'long'.")

@app.route('/generate', methods=['POST'])
def generate_media_sentences():
    data = request.json
    media_type = data.get("media_type")
    genre = data.get("genre")
    japanese_word = data.get("japanese_word")
    length = data.get("length")
    
    max_tokens = determine_max_tokens(length)
    
    if media_type == "book":
        system_message = f"You are a writer creating a {genre} book. Generate a story in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "news":
        system_message = f"You are a journalist writing a {genre} news article. Generate a news segment in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "movie":
        system_message = f"You are a screenwriter writing a {genre} movie. Generate a dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "anime":
        system_message = f"You are a scriptwriter creating a {genre} anime. Generate a dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "manga":
        system_message = f"You are a mangaka creating a {genre} manga. Generate a dialogue in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "tv show":
        system_message = f"You are a scriptwriter creating a {genre} TV show. Generate a dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "game":
        system_message = f"You are a game writer creating a {genre} RPG game. Generate a dialogue or narration in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."
    elif media_type == "music":
        system_message = f"You are a songwriter creating a {genre} song. Generate a song lyric or stanza in Japanese fitting this genre that includes the word '{japanese_word}' in {max_tokens} tokens, no additional text."

    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=system_message,
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2
    )
    
    japanese_sentence = response.choices[0].text.strip()
    
    translation_response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=f"Translate the following Japanese sentence to English: {japanese_sentence}",
        temperature=0.7,
        max_tokens=256,
        top_p=1
    )
    
    english_translation = translation_response.choices[0].text.strip()
    
    return jsonify({
        "sentence": japanese_sentence,
        "translation": english_translation
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

