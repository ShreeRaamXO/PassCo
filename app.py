from flask import Flask, render_template, request, jsonify
from utils.generator import generate_passphrase, calculate_entropy, load_wordlist
from utils.security import estimate_crack_time, check_pwned, calculate_password_entropy

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    num_words = int(request.form.get("words", 4))
    passphrase = generate_passphrase(num_words)
    entropy = calculate_entropy(num_words, len(load_wordlist()))
    crack_times = estimate_crack_time(entropy)
    pwned_status = check_pwned(passphrase)

    return jsonify({
        "passphrase": passphrase,
        "entropy": entropy,
        "crack_times": crack_times,
        "pwned_status": pwned_status
    })

@app.route("/check_entropy", methods=["POST"])
def check_entropy():
    password = request.form.get("password", "")
    entropy = calculate_password_entropy(password)
    crack_times = estimate_crack_time(entropy)
    pwned_status = check_pwned(password)

    return jsonify({
        "password": password,
        "entropy": entropy,
        "crack_times": crack_times,
        "pwned_status": pwned_status
    })

if __name__ == "__main__":
    app.run(debug=True)
