from flask import Flask, render_template, request, jsonify
import openai


app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'


# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("bo2.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    if completion.choices[0].message['content'] is not None:
        return jsonify({"message": completion.choices[0].message['content']})

    else :
        return 'Failed to Generate response!'
    

if __name__=='__main__':
    app.run()
