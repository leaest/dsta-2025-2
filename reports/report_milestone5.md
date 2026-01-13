# Milestone 5

## 0 - New Requirements
|Package Name|Version|SHA-256|
|---|---|---|
|...|...|...|
|...|...|...|
|...|...|...|
|...|...|...|

## 1 - Flask Application
### Notes so far
We can use a JSON file to pass the Postgres database detail to the APi. It has the following structure:
  {
    "postgres": {
      "DB_HOST": "localhost",
      "DB_PORT": 5432,
      "DB_NAME": "dsta_ms5",
      "DB_USER": "user",
      "DB_PASSWORD": "password",
      "DB_TABLE": "mnist"
    }
  }

**main.py**
This document is used to create the Flask applicatoin.

At the beginning the databse and application configuration is loaded from the JSON file followed by database-related setitngs. We use the formulas defined in `db_utils` o initialize the DB table. Then we try to loads the model if it exists in the specified path.

Root: Landing endpoint so see if the API is running
Read: Retrieves all rows form the DB table and returns them as JSON
Prediciton: Allows clients to send data to be inserted into the database. Image(s) are decoded and processed to be predicted. The last step stores the raw image bytes, true and predicted label.

The last step is the application entry point which starts the Flask development server. `0.0.0.0` allows the access from outside the machine (for docker i think?).



### REST Endpoint
**Expose**

**Accept POST Request**

### Send Image

### Accept Image

### Return Prediction