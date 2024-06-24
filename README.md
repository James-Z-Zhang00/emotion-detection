# Emotion Detection Web Application

A Web Application project to analyze emotions from user-provided textual data, identify dominant emotion.

CRUD operations embedded with dynamic http requests.

## Objectives

Develop a Python package that processes string variable with IBM Watson NLP (Natural Language Processing) Libraries, return the emotion analysis in a JSON file.

Create a front end UI for the user to enter text message, sent the http request and display the analysis results.

Build a Python UnitTest module to test the program.

Improve the program by Pylint in PEP8 Guidelines.

Deploy the app by Python Flask framework.

## Emotion Analysis

The feature that get the emotion report and sent the formatted data back to the UI with IBM Watson Natural Language Processing.

```python
def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # url for using IBM Watson NLP libraries
    inputJson = { "raw_document": { "text": text_to_analyse } }
    # Create JSON file for the library to proceed analysis
    Headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    # Create the header of request before sending
    response = requests.post(url, json = inputJson, headers = Headers)
    # Send the request by POST method to the url we defined before, with the given JSON file and the header
    formatted_response = json.loads(response.text)
    # Extract the text part of the response and convert it to JSON

    if response.status_code == 400 or response.status_code == 304:
    # Error handling: if there's an error (invaild text input or page not found)
        for f in formatted_response:
            formatted_response[f] = None
        formatted_response['dominant_emotion'] = None
        # Set all attributes of the response to None and add key-value pair dominant_emotion : None
        # For the UI to know there's an invaild return
        return formatted_response
        # Return the response from here, the function will not go any further
        
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    # Extract the emotion part of the response JSON
    dominant_emotion = _get_dominant_emotion(emotions)
    # Get the dominant emotion (the emotion with the highest score)
    emotions['dominant_emotion'] = str(dominant_emotion)
    # Set the dominant_emotion data
    return emotions
    # Return the response to the UI
```

User with authentication can access to:
- `customer/auth/review/`

User authentication process:
1. Send POST request with username & password `/register`
2. Server save the username & password into database (a list in this project), the server will send *user register successful* message
3. Send POST request with username & password `customer/login`
4. Once the username & password validated, the server will send JWT (JSON Web Token) to the request sender, the token will be valid in 60 minutes
5. Now the user can pass the `customer/auth/*` middleware then access to authorization required routers

Router to handle user registeration

```js
public_users.post("/register", (req,res) => {
  const username = req.body.username;
  const password = req.body.password;
  if (username && password) {
    // username validation
    if (doesExist(username)) { 
      return res.status(404).json({message: "Username already exists!"});   
    } else {
      users.push({"username":username,"password":password});
      return res.status(200).json({message: "Customer successfully registred. Now you can login"});
    }
  } 
  return res.status(404).json({message: "Unable to register user, both username and password must be filled!"});
});
```

Postman (testing tool) screenshot, where username and password were sent by JSON

<img width="521" alt="register" src="https://github.com/James-Z-Zhang00/book-review-server/assets/144994336/d36e71cd-e439-4dbd-84cf-e2a2a0576da5">

User authentication process

```js
//only registered users can login
regd_users.post("/login", (req,res) => {
  const username = req.body.username;
  const password = req.body.password;
    if (authenticatedUser(username, password)) {
    // If the username and password passed checking
    currentUsername = username;
    // Sign the JWT (JSON Web Token) to generate accessToken with the given username
    // With 60 * 60 available time (1 hour)
    let accessToken = jwt.sign({
            data: username,
        }, 'access', { expiresIn: 60 * 60 });

        // Set the access token and username in the session
        req.session.authorization = {
            accessToken: accessToken,
        };
    // Return registeration successful message back to the user
    return res.status(200).send("Customer successfully logged in\n");
    }
    // Return the failed login message back to the user
    res.status(401).send("No such username and password combination!");
});

// Check if the user send correct username and password
const authenticatedUser = (username,password)=>{ 
  let validusers = users.filter((user)=>{
    return (user.username === username && user.password === password)
  });
  if(validusers.length > 0){
    return true;
  } else {
    return false;
  }
}
```

Postman testing for user login

<img width="549" alt="login" src="https://github.com/James-Z-Zhang00/book-review-server/assets/144994336/9d3437bd-a6a8-4810-aa47-d65aff7f2217">

After authentication, user can:
1. Post new review for a book
2. Update or delete an existing review that posted by the _same_ user previously
