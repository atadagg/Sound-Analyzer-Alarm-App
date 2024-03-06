## What is this?

This is an alarm app that's triggered by sound. Currently the alarm is triggered by desibel. 

## Why would I need this?

If you ever went to a dorm hostel or you had to sleep outside for some reason, this app will wake you up everytime there are people moving around you. Especially useful if you're alone and carrying valuables. (I actually needed an app like this one time and couldn't find it that's why I built this.)

## Technicalities

I've used the Kivy library of Python to be able to ship this app into all platforms.
For sound analysis I've used PyAudio and NumPy.

## Future of the project

This is a project that I'm actively developing right now. 
I'm planning to make the sound analysis using audio classification with machine learning to recognize things like footsteps, clanks and other noises awake humans make.