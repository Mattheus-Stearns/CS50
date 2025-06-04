# Google Automation Web Application
#### Video Demo: https://youtu.be/LRpmZoJ9UBA?si=NzSWTLThflmeUgj-
#### Description:
This project is a basic web application that was used to teach myself how to use google api's. So, I incorporated six different functions, calling the Google Mail, Google Calendar, Google Docs, Google Sheets, Google Forms APIs, as well as implementing an old search function, as an homage to one of the excercises in the class and another homage to a older version of google search. 

These APIs are all maintainted and authenticated by OAuth, which is forced upon the user as the only way to sign in to the WebApp is with a google sign in. 

I feel like what I got out of this project was much more familiarity with web application programming, as well as google's APIs. 

Let's dive into the different functions shall we?

Google Mail:

I just grabbed a library that validated that the google mail addresses were in the correct format, and once I realized that it was necessary to pay to check if those emaols were actually in service I decided that there was enough checking. Then I made a dict of possible errors, which I did in a similar way for all of the other functions as well. Then I tried to get the user's credentials and check if they had authenticated the API or fully signed in.

Then I implemented a function in JavaScript that I went and used for almost every function that would redirect the page to the home page if the API resolved successfully. Simultaneously, it would open the effected google app. This made it very much easier for the user to validate that the code worked as well.

Google Calendar:

Building off of all of the work done in the previous function of my app, I had to manage the time: both the user's and the server's - so that I could precisely log what time the user wanted to do the event in, and no issue would arise due to timezones. To identify the user's timezone I had to use a hidden form attatched to some JavaScript that would tell me the timezone that the user is in, and I was able to use that to record the time on the calendar for the event, local for the user.

Google Docs:

Google Sheets:

Google Forms:

Google Search:
