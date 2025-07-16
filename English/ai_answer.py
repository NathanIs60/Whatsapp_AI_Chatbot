import openai

openai.api_key = ""#Your API KEY

def ai_message_answer(message):
    try:
        response = openai.chat.completions.create(  # For creating the ChatBot; in older versions, ".ChatCompletions" may be used
            model="gpt-3.5-turbo",  # ChatBot Model
            messages=[
                {"role": "system", "content": "You are a chatbot that speaks like a friend."},  # ChatBot Role Section
                {"role": "user", "content": message}
            ]
        )
        return response['choices'][0]['message']['content']  # Return the response from the API
    except Exception as e:
        print("Error:", e)
        return "Response could not be generated"
# You can get your API key from the official OpenAI page based on your pricing plan, or use another compatible API.
