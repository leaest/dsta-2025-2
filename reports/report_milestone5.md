# Milestone 5

## 0 - New Requirements
|Package Name|Version|SHA-256|
|---|---|---|
|Flask|3.1.2|78a7b7e58bc7e5e5b21ea3925c0285b0325a203ff688f3381b50bfbac61b7ad3|


## 1 - Flask Application
**main.py**
This document is used to create the Flask application.

At the beginning the database and application configuration is loaded We use the formulas defined in `db_utils.py` to initialize the DB table. The formula for creating the database and the initialization are exactly the same as in milestone 3. This means there is a table for the input data and a separate table for the prediction.
Also like in milestone 3, the model was loaded with the function defined in `model_utils.py`.

After these first apps, the flask application was created.
The first function 
The root displays a welcome page:
```python
@app.route("/")
def home():
    return '''
    <h1>Welcome to our App!</h1>
    <h2>The Website to upload an image would be here</h2>
    '''
```
defines the html that is returned when someone visits the [root]http://localhost:5000/ of the flask application.

The second function `read()` uses a GET request, in which it sends a request to the API, that then tries to output the last predictions made from the database. 

The third function, is the function that is most important for this task and it does several things.
**Error Message**
If the provided data is not a pictures, it prints a error message.

**Image Decoding**
If the posted data is indeed a image, it first saves the "image"-data from HTTP-Body that was "transmitted". The base64 format is then converted into binary code. Since the model was trained on a deserialized image, this conversion must take place. However, since our image is stored in a binary format now, a new function was added to `image_utils.py`, which is able to convert the binary format to a numpy array. The 2D array from the function is then reshaped into the 4D array (1, 28, 28, 1).

**Database**
This array is then passed to the trained model and defines stores the prediction (with the highest probability).
It then creates a connection to the Postgres Database based on with the functions from `db_utils.py`.
It then inserts the image (in binary format) into the input_data table, the input_id is a auto-generated id (to connect the tables). In the second table this input_id and the predicted label are stored. Then the prediction is returned.

**Port- and Host-Settings**
The last step is the application entry point which starts the Flask development server. `0.0.0.0` allows the access from outside the container by making Flask listen on all network interfaces and not just the container's local host. The port defines to which port the Flask application is mapped to inside the container.
If only the port mapping was configured and not the host, it would only listen on the internal port. When our computers would try to "talk" to the container, Flask will only be listening to internal port-requests and the connection would be refused because then Docker can't forward it (Docker always forwards to the external port), on which without `0.0.0.0` won't be listening.


### REST Endpoint
**Expose**

**Accept POST Request**
