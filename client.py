import openai

# Initialize the OpenAI client with your API key
openai.api_key = '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'  # Replace this with your actual API key

async def get_completion():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like alexa and google cloud"},
                {"role": "user", "content": "what is coding"},
            ],
        )

        # Output the completion result
        print(response['choices'][0]['message']['content'])

    except Exception as e:
        print(f"Error: {e}")

# Call the function
if __name__ == "__main__":
    import asyncio
    asyncio.run(get_completion())
