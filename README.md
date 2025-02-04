# Number Properties API

A simple Flask API that takes a number and returns interesting mathematical properties, along with a fun fact.

## Features

- Check if a number is prime or perfect
- Identify number properties (even/odd, Armstrong number)
- Calculate digit sum
- Fetch fun math facts about the number using [Numbers API](http://numbersapi.com/#42)

## Local Setup 
1.  Clone the repository
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the application: `python app.py`

## API Documentation

### Endpoints
`GET /api/classify-number?number={num}`

-   Retrives number mathematical properties
-   Supports all valid integers

## Example Usage

#### Using cURL
```bash
curl "http://127.0.0.1:5000/api/classify-number?number=678"
```

## Response Example
```json
{
  "digit_sum": 21,
  "fun_fact": "678 is a member of the Fibonacci-type sequence starting with 1 and 7.",
  "is_perfect": false,
  "is_prime": false,
  "number": 678,
  "properties": [
    "even"
  ]
}
```

## Error Handling

The API returns standard HTTP status codes:
- 200: Successful request
- 500: Server error

## Deployment
-   Deployed using Gunicorn
-   CORS enabled for cross-origin requests
-   Deployed with render

## Technologies
-   Python
-   Flask
-   Requests Library
-   Numbers API

## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Make your changes and commit (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature-branch`).
5.  Create a pull request.

## License

This project is licensed under the MIT License.