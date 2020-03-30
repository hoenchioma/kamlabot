# kamlabot
Helper chatbot for fetching various useful info (like class routine, syllabus, etc.)

This chatbot's creation came from the idea, to alleviate the need to ask the class representative/monitor, teacher, or other students about commonly needed class info like class routine, syllabus, books, materials, etc.

### Platforms
Up until now, it supports two messaging platforms namely [facebook messenger](https://www.messenger.com/) and [discord](https://discordapp.com/). I have plans to add more in the future.

### How it works
The working procedure is crudely described below:
- Bot fetches message from respective messaging platform
- Uses NLP (powered by [wit.ai](https://wit.ai)) to figure out what the message is trying to say
- Fetches relevant data from [Firebase Realtime Database](https://firebase.google.com/docs/database) (which was placed there during the setup phase) and sends it back to the relevant messaging platform.

The data stored in Firebase can be updated when needed without needing to touch the actual server application.

### How to setup
#### 1. Get necessary configs
Before deploying server you will need to set some environment variables corresponding to some API configurations
1. `FB_ACCESS_TOKEN` and `FB_VERIFY_TOKEN` : Facebook page access token and verfication token for message authentication.
You can find how to setup a Facebook application and get the above tokens [here](https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start).
(You can skip this if you're not using the messenger server)
2. `DISCORD_TOKEN` : Discord app token. (You can skip this if you're not using the discord server)
3. `WIT_AI_CLIENT_TOKEN` : [wit.ai](https://wit.ai)'s client access token. Can be found in the settings page of your wit.ai app.
4. `FIREBASE_PROJECT_ID` and `FIREBASE_CONFIG` : The firebase project name and the config json respectively.

#### 2. Deploy server
You can deploy this server anywhere you wish. I personally used [heroku](https://heroku.com/) since it was free I didn't have many concurrent users.

*Note: You will need Python v3.3 or higher*

First of all install the dependencies
```
pip3 install -r requirements.txt
```

The messenger_server is a Flask server which you can run using
```
gunicorn kamlabot.messenger_server:app
```
You can run the discord server by simply running
```
python3 -m kamlabot.discord_server
```
For heroku you can run both in a single dyno by placing the following in the Procfile
```
web: gunicorn kamlabot.messenger_server:app & python3 -m kamlabot.discord_server & wait
```
