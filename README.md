# Creating your J.A.R.V.I.S personal assistant with Python

Reference: https://www.freecodecamp.org/news/python-project-how-to-build-your-own-jarvis-using-python/

## 1 ) Environment Setup

First, create your virtual env. You can do it using <code>virtualvenv</code> or using conda distribution

#### - 1.a) Using virtualenv:

To create a virtual environment using <code>virtualvenv</code>, you can use the below command

```shell script
$ python -m venv env
```

The above command will create a virtual environment named <code>env</code>. Now, we need to activate the environment using the command:

```shell script
$ . env/Scripts/activate
```

To verify if the environment has been activated or not, you can see <code>(env)</code> in your terminal.

#### - 1.b) Using conda environment

One can also use conda to create a virtual enviroment. To do this, use the command below in the terminal (you need a conda distribution installend in your machine):

```shell script
$ conda create --name env python=3.9
```

The above command will create a virtual environment named <code>env</code> with python 3.9.x. To activate the environment, use the following command:

```shell script
$ conda activate env
```

To verify if the environment has been activated, you canse the <code>(env)</code> in your terminal.

## 2 ) Installing the libraries

#### 1. <ins>pyttsx3</ins>:

pyttsx is a cross-platform texto to speech library which is platform-independet. The major advantage of using this library for text-to-speech conversion is that it works offline. To install this module, type the below command in the terminal:

```shell script
$ pip install pyttsx3
```

#### 2. <ins>SpeechRecognition</ins>:

This allows us to convert audio into text for futher processing. To install this module, type the below command in the terminal:

```shell script
$ pip install SoeechRecognition
```

#### 3. <ins>pywhatkit</ins>:

This is an easy-to-use library that will help us interact with the browser very eaasily. To install the module, run the following command in the terminal:

```shell script
$ pip install pywhatkit
```

#### 4. <ins>wikipedia</ins>:

We'll use this to fetch a variety of information from the Wikipedia website. To install this module, type the below command in the terminal

```shell script
$ pip install wikipedia
```

#### 5. <ins>requests</ins>:

This is an elegant and simple HTTP library for Python that allows you to sent HTTP/1.1 requests extremely easily. To install the module, run the gollowing command in the terminal:

```shell script
$ pip install requests
```

## 3 ) .env File

We need this file to store some privater data such as API Keys, Passwords, and so on that are related to the project. for now, let's store the name of the user and the bot.

Create a file named .env and add the following content there

```
USER=Ashutosh
BOTNAME=JARVIS
```

To use the contents from the <code>.env</code> file, we'll install another module called **python-decouple** as:

```shell script
$ pip install python-decouple
```

## 4) How to Set Up JARVIS with Python

Before we start defining a few important functions, let's create a speech engine first.

```python
import pyttsx3
from decouple import config

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init()

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
```

Let's analyze the above script. First of all, we have initialized an <code>engine</code> using the <code>pyttsx3</code> module. <code>sapi5</code> is a Microsft Speech API that helps us use the voices. Learn more about it [here](<https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ee125663(v=vs.85)>).

NOTE: If your system is Linux-based (e. g. Ubuntu), you may have to install a espeak, a speech synthesizer compatible with pyttsx3. You can install using the below command:

```shell script
sudo apt-get install espeak
```

Next, we are setting the `rate` and `volume` properties of the speech engine using `setProperty` method.

Now, we can get the voices from the engine using the `getProperty` method. `voices` will be a list of voices avaiable in our system. If we print it, we can see as below

```
[<pyttsx3.voice.Voice object at 0x000001AB9FB834F0>, <pyttsx3.voice.Voice object at 0x000001AB9FB83490>]
```

### Enable the Speak Function

The speak function will be responsible for speaking whatever text is passed to it. Let's see the code:

```python
# Text to Speech Conversion
def speak(text):
  """Used to speak whatever thext is passed to it"""

  engine.say(text)
  engine.runandWait()
```

In the `speak()` method, the engine speakes whatever text is passed to it using the `say()` method. Using the `runAndWait()` method, it blocks during the event loop and returns when the commands queue is cleared.

### Enable the Greet Function

This function will be used to greet the user whenever the program is run. According to the current time, it greets Good Morning, Good Afternoon, or Good Evening to the user.

```python
from datetime import datetime


def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")
```

First, we get the current hour, that is if the current time is 11:15AM, the hour will be 11. if the value of hour is between 6 and 12, wish Good Morning to the user. if the value is between 12 and 16, wish Good Afternoon and similarly, if the value is between 16 and 19, wish Good Evening. We are using the speak method to speak to the user.

### Hot to Take User Input

We use this function to take the commands from the user and recognize the command using the `speech_recognition` module.

```python
import speech_recognition as sr
from random import choice
from utils import opening_text


def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query
```

We have imported `speech_recognition` module as `sr`. The Recognizer class within the `speech_recognition` module helps us recognize the audio. The smae module has a Microphone class that gives us access to the microphone of the device. so with the microphone as the `source`, we try to listen to the audio using the `listen()` method in the Recognizer class.

We have also the the `pause_threshhold` to 1, that is it will not complai even if we pause for one second during we speak.

Next, using the `recognize_google()` method from the Recognizer class, we try to recognize the audio. The `recognize_google()` method perfoms speech recognition on the audio passed to it, using the **Google Speech Recognition API**.

We have set the language to **en-in**, which is English India. It returns the transcript of the audio which is nothing but a string. We've stired ut ub a variable called `query`. You can also change the language to your native speak. check the avaiable languages [here](http://stackoverflow.com/a/14302134).

If hte query haas **exit** or **stop** in it, it means we're asking the assistant to stop immediately. So, before stopping, we greet the user aagain as per the current hour. If the hour is between 21 and 6, wish Good Night to the user, else, some other message.

We create a `utils.py` file which has just one list containing a few statements like this:

```python
opening_text = [
    "Cool, I'm on it sirt.",
    "Okay sir, I'm working on it.",
    "Just a second sir,",
]
```

If the query doesn't have those two words(exit or stop),we speak something to tell the user that we haver heard them. for that, we will use the choice method from the random module to randomly select any statement from the `opening_text` list. After speaking, we exit from the program.

During this entire process, if we encounter an excepetion, we apologize to the user and set the `query` to None. In the end, we return the `query`.

## How to Set Up Offline Functions

Inside the `functions` folder, create a Python file called `os_ops.py`. In this file, we'll create various functions to interact with the OS.

```python
import os
import subprocess as sp

paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}
```

In the above script, we have created a dictionary called `paths` which has a software name as the key and its path as the value. You can change the paths according to your system and add more software paths if you need to do so.

### How to Open the Camera

We'll use this function to open the camera in our system. We'll be using the `subprocess` moule to run the command

```python
def open_camera():
    sp.run('start microsoft.windows.camera', shell=True)
```

### How to Open Notepad and Discord

We'çç use these functions to open Notepad++ and Discord in the system.

```python
def open_notepad():
    os.startfile(paths['notepad'])


def open_discord():
    os.startfile(paths['discord'])
```

### How to Open the Command Prompt

We'll use this function to open the command prompt in on our system.

```python
def open_cmd():
    os.system('start cmd')
```

### How to Open the Calculator

We'll use this function to open the calculator on our system.

```python
def open_cmd():
    os.syst
```

## How to Set Up Online Functions

We'll be adding several online functions. They are:

1. Find my IP address
2. Search on Wikipedia
3. Play videos on YouTube
4. Search on Google
5. Send WhatsApp message
6. Send Email
7. Get Latest News Headlines
8. Get Weather Report
9. Get Trending Movies
10. Get Random Jokes
11. Get Random Advice
