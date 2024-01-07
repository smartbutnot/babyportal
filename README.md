# babyportal

We started using the "babytracker" app by nighp when we had our baby, to keep track of feeds, nappies and so on. We use it on iPhones and APple Watches, but I have a bunch of RGB LED matrixes from other projects and thought it would be useful to be able to glance at them and see how long since he's been fed, or whatever. Helpful when you don't have your hands free, or don't want to reach over in bed.

So! First problem is how to get data out of the app. The app (which I recommend btw) lets you export to CSV or backup the account, but doesn't have a real time API. I ended up using an Android VM and inspecting the database every couple of minutes.

Second problem is how to turn the database into a small number of useful values. I hacked together some sqlite queries to produce things like the number of poos he's done today in total.

Then it's fairly easy - I publish those values to an MQTT server, and the matrix runs some circuit python to display them with some icons. All the code is in the repository - babytracker.py does the data extraction and the matrixportal code displays it on an adafruit matrixportal M4.


