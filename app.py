import os
import math  # for sqrt
import requests  # to make http requests to numbers api
import logging
import regex as re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)


def is_armstrong_number(num):
    """Check if a number is an Armstrong number."""
    num_str = str(num)  # convert the number to a string
    n = len(num_str)
    # find the sum of each digit raised to power of number of digits
    return num == sum(int(digit) ** n for digit in num_str)


def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def is_perfect(num):
    """check if it's a perfect number"""
    # A number is a perfect number if is equal to sum of its proper divisors excluding itself
    if num < 2:
        return False
    divisor_sum = sum([x for x in range(1, num // 2 + 1) if num % x == 0])
    return divisor_sum == num


def get_number_properties(num):
    """Get various properties of a number."""
    properties = []

    # Check if even/odd
    properties.append("even" if num % 2 == 0 else "odd")

    # Check for Armstrong number
    if is_armstrong_number(num):
        properties.append("armstrong")
    return properties
    # Should look like
    # For 371: ['odd', 'armstrong']
    # For 8: ['even']


def digit_sum(num):
    """Get the sum of the digits"""
    return sum(int(digit) for digit in str(num))


def get_fun_fact(num):
    """Fetch a fun fact from Numbers API."""
    try:
        # Make GET request to Numbers API
        response = requests.get(f"http://numbersapi.com/{num}/math")
        # Return fact if successful, otherwise return error message
        return (
            response.text if response.status_code == 200 else "No fun fact available."
        )
    except Exception:
        return "Unable to fetch fun fact."


@app.route('/')
def home():
    return jsonify({"message": "Number Properties API is running"})


@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify a number and return its properties."""
    try:
        # Figure how to get number from query parameter
        num_str = request.args.get('number')
        logging.info(f"Received number: {num_str}")  # Add logging

        # Check if 'number' parameter is missing
        if num_str is None:
            return jsonify({"number": "", "error": True}), 400
        if not re.match(r"^[-+]?\d+$", num_str): 
            return jsonify({"number": num_str, "error": True}), 400

        # Validate input if its an integer
        try:
            num = int(num_str)
            if num < 0:  # Handle negative numbers
                return jsonify({"number": num_str, "error": "Number must be positive"}), 400
        except ValueError:
            return jsonify({"number": num_str, "error": True}), 400

        # Gather number properties
        # figure how to keep json response ordered
        return (
            jsonify(
                {
                    "number": num,
                    "is_prime": is_prime(num),
                    "is_perfect": is_perfect(num),
                    "properties": get_number_properties(num),
                    "digit_sum": digit_sum(num),
                    "fun_fact": get_fun_fact(num),
                }
            ),
            200,
        )

    except Exception as e:
        logging.error(f"Server Error: {e}")
        return jsonify({"error": True, "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True)
