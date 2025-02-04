import math  # for sqrt
import requests  # to make http requests to numbers api
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def is_armstrong_number(num):
    """Check if a number is an Armstrong number."""
    num_str = str(num)   # convert the number to a string
    n = len(num_str)
    # find the sum of each digit raised to power of number of digits
    # Example:
    # For 371: 3³ + 7³ + 1³ = 27 + 343 + 1 = 371 (is Armstrong)
    # For 123: 1³ + 2³ + 3³ = 1 + 8 + 27 = 36 (not Armstrong)
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
    properties.append('even' if num % 2 == 0 else 'odd')
    
    # Check for Armstrong number
    if is_armstrong_number(num):
        properties.append('armstrong')
    
    return properties
    # Should look like
    # For 371: ['odd', 'armstrong']
    # For 8: ['even']


def get_fun_fact(num):
    """Fetch a fun fact from Numbers API."""
    try:
        # Make GET request to Numbers API
        response = requests.get(f'http://numbersapi.com/{num}/math')
        # Return fact if successful, otherwise return error message
        return response.text if response.status_code == 200 else "No fun fact available."
    except Exception:
        return "Unable to fetch fun fact."


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify a number and return its properties."""
    try:
        # Figure how to get number from query parameter 
        num_str = request.args.get('number', '')
       
        # Validate input
        try:
            num = int(num_str)
        except ValueError:
            return jsonify({
                "number": num_str,
                "error": True
            }), 400
        
        # Gather number properties
        # figure how to keep json response ordered
        return jsonify({
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect(num),
            "properties": get_number_properties(num),
            "digit_sum": sum(int(digit) for digit in str(num)),
            "fun_fact": get_fun_fact(num)
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_type": True
        }), 500


@app.route('/test')
def test():
    return "Hello from test!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
