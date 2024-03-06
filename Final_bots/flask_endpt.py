from flask import Flask, request, jsonify
import openai
import os
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

initial_prompt = "You are a real estate investment expert specializing in commercial real estate in delhi ncr region. Start by taking the name and phone number of the user. Assist users in understanding the right investment for them and assisting them with the best option for that nature of investment. Finalizing upto 3 projects and schedule a visit. only access primary market commercial projects."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", None)

    if user_input is not None and user_input.strip() != "":
        messages = [{"role": "system", "content": initial_prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=messages,
            max_tokens=600,
            temperature=1,
        )

        chat_history = [
            {"role": "user", "content": user_input},
            {
                "role": "assistant",
                "content": response.choices[0].message.content.strip(),
            },
        ]

        return jsonify({"chat_history": chat_history})
    else:
        return jsonify({"error": "Invalid input"}), 400


# if __name__ == "__main__":
#     app.run(debug=True)
