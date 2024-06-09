# Subfeddit-Sentiment-Analysis

This microservice provides a RESTful API to analyze and classify comments from a given subfeddit as positive or negative based on their polarity score.

## Features

- Retrieve the most recent 25 comments for a given subfeddit.
- Optionally filter comments by a specific time range.
- Optionally sort the results by the comments' polarity score.

## API Endpoints

### GET `/api/v1/subfeddit_category`

#### Query Parameters

- `subfeddit_name` (mandatory): The name of the subfeddit.
- `start_date` (optional): The start date for filtering comments.
- `end_date` (optional): The end date for filtering comments.
- `sort_by_polarity` (optional): Boolean to sort results by polarity score.

#### Example Request

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/subfeddit_catagory?subfeddit_name=Dummy%20Topic%201&sort_by_polarity=true' \
  -H 'accept: application/json'
```
#### Pre-requisite
Please run the feddit-api application before run this fastapi application.

#### To Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### To Install Dependencies

```bash
pip install -r requirements.txt
```

#### Run the application:

```bash
  python main.py
```

#### To run the tests, use:

```bash
  python -m unittest discover -s .
```






