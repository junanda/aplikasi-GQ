from flask import Flask


app = Flask()
app.secret_key = "lansdjkacnkaj1234"

if __name__ == "__main__":
    app.run(debug=True)
