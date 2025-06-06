# Google Automation Web Application
#### Video Demo: https://youtu.be/LRpmZoJ9UBA?si=NzSWTLThflmeUgj-
#### Description:
This project is a basic web application that was used to teach myself how to use google api's. So, I incorporated six different functions, calling the Google Mail, Google Calendar, Google Docs, Google Sheets, Google Forms APIs, as well as implementing an old search function, as an homage to one of the excercises in the class and another homage to a older version of google search. 

These APIs are all maintainted and authenticated by OAuth, which is forced upon the user as the only way to sign in to the WebApp is with a google sign in. 

I feel like what I got out of this project was much more familiarity with web application programming, as well as google's APIs. 

Let's dive into the different functions shall we?

Google Mail:

I just grabbed a library that validated that the google mail addresses were in the correct format, and once I realized that it was necessary to pay to check if those emails were actually in service I decided that there was enough checking. Then I made a dict of possible errors, which I did in a similar way for all of the other functions as well. Then I tried to get the user's credentials and check if they had authenticated the API or fully signed in.

Then I implemented a function in JavaScript that I went and used for almost every function that would redirect the page to the home page if the API resolved successfully. Simultaneously, it would open the effected google app. This made it very much easier for the user to validate that the code worked as well.

Google Calendar:

Building off of all of the work done in the previous function of my app, I had to manage the time: both the user's and the server's - so that I could precisely log what time the user wanted to do the event in, and ensure that no issue would arise as a result of timezones. To identify the user's timezone I had to use a hidden form attatched to some JavaScript that would tell me the timezone that the user is in, and I was able to use that to record the time on the calendar for the event, local for the user.

I also ran into some trouble in regards to trying to find the url of the google calenedar event that would be used to redirect the user upon completion - I was trying to access a variable that didn't exist: while I had called the function, and events were created in the user's google calendar, initially, I did not save the results to a variable to call the function that would give me the url on. That required some googling and ai to figure out.

Google Docs:

This is where I started making regex variables so that with form submission I would be able to convert the user submission of the google doc link to exactly how I wanted it to be. This also made it relatively easy, through a subtractive process, to get rid of the occurence of the user sumbitted link expressed in the regex variable and be left with the document's id, which is imperatoive to have so that google's docs api can work, and is harder to ask the user for outright, lest they misunderstand. 

One thing that I had to find by trial and error is the different variable names that google uses on the developers' side to relate to what the user sees. I had to ensure that I was appending to google docs, and not just writing a blanck copy every time, because if users' docs were wiped they would not be happy. 

Google Sheets:

After doing google docs, google sheets was much easier. There was not anything expressely unique to the google sheets api, except that the service is on v4 and that you have to handle expressely the cell in which the inserting is taking place. Here I decided it was best to go for insertion, (thus wiping any data previously in that cell) because then that could handle inserting more data broadly in the sheets but also updating specific cells.

Google Forms:

Google forms was a bit complex in that google encourages people to be linking google sheets api and google forms together, and then mainly using google sheets to hamndle all of the responses, and I tried that out but it didn't feel authentic, nor was I actually even using google forms api. So then I decided that I would try and do one of the few things that google forms api does support: getting a json of all of the responses to a form, which the user gives the url of.

This means that there was very little error handling to be done, because all I had to check was that the user responded and responded according to the regex that I made for google forms links. There was also very little that needed to be done to build the service, except I did have to make a concerted effort to sava a dict of all of the responses, and then passed that to my template, so that the jinjia could iterate over it and display everything in a table. 

Google Search:

Implimenting google search was really fun. I realized quickly that google did not have a google search api, but I remembered one of the classes where we implimented a more basic form of a google search by formatting a response in a string, following search?q=. I wanted to impliment the google search that I was familiar with in 2011, so I took a users input, and made sure that if there were spaces that they would be replaced with pluses (thats how google handles whitespace in its url) and then just redirected the user to the string that I had built. 

I remembered that there was a "I'm feeling lucky" button in 2011, so I searched how to impliment that online, and it was relatively simple. Then I finally had the same search that I was looking at in 2011! How nolstalgic.

Thanks:

Taking CS50 has been a journey, and a journey that I would never regret taking. There were many nights that made me stay up way past midnight, pulling my hair out and accelerating my receding hairline (particularly when I was tasked with keeping the safety of fiftyville). While I have had a lot of passive programming experience in the past, seen by the fact that I always completed the hard problems, CS50 took my basic knowledge of lists and taught me about how they are handled at the lowest level, but also how they are handled at a much higher level, just as an example.

For that reason I want to thank David Malan for being an awesome host to this journey, at the helm for a significant amount of time, and I also want to thank Finn Olsen, who tried to take CS50 after I did, and while he completed CS50P he didn't fare so well in CS50. Even though he couldn't do CS50, we still met up frequently and he would always listen to my compplaints about running into issues compiling on apple metal. 

Finally, thanks to me, who had the courage to take CS50 in the last semester of my high school, and while most of my friends were split between drinking, studying, and sleeping, I was coding, studying, and sleeping. Oh right, drinking as well of course. <3 