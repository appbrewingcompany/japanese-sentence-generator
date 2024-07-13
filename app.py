import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = 'your_openai_api_key'  # Replace with your OpenAI API key

# Function to generate example sentences
def generate_example_sentences(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a Japanese word, topic, sub-topic, difficulty level, and formality level, and your task is to generate a random Japanese example sentences based on those criteria alongside its English translation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1.4,
        max_tokens=64,
        top_p=1
    )
    return response

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    japanese_word = data.get('japanese_word')
    topic = data.get('topic')
    sub_topic = data.get('sub_topic')
    difficulty_level = data.get('difficulty_level')
    formality_level = data.get('formality_level')

    prompt = f"Japanese Word: {japanese_word} \n topic: {topic} \n sub-topic: {sub_topic} \n difficulty level: {difficulty_level} \n formality level: {formality_level}"
    response = generate_example_sentences(prompt)
    return jsonify(response.choices[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
