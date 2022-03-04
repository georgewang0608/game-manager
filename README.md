# Homework 7 - Flask with User Input and APIs
Due: 8 December, 5pm (but, as this does not have solutions, the deadline is flexible)

We can be flexible out this deadline; we're suggesting the 7th as a good milestone toward having a strong project.

What to hand in: 
- A link to your GitHub repository, including all of your code, including any images, HTML templates, CSS, and app.yaml files we need to run your program.
- You can use Canvas as a backup turn in, but if so, please zip all the files rather than turning them in separately -- especially because folders matter!
- If you get your code running on Google Cloud, we'd love a link to it there too!

Even if you are working with a partner on your project, this is an individual assignment. You are, as always, encouraged to collaborate - but you should write your own code and be able to explain all code in your assignment in your own words.

# The assignment
This assignment is a bit different. You goal is to write a Flask App that
1. Accesses an API (not the sunrise/sunset API or the National Weather Service API) to retrieve results.
2. Accepts user input that affects what it searches for and/or what results it shows.

This assignment is written to be as flexible as possible, so that you can use any of the following as a starting point:
- HW6 (in which case, the most basic version of the app will search Flickr for a tag and display some images), 
- Your HW5 Part 2, or
- Some other API, if your project idea has changed since HW5 Part 2.

and get it running in Flask. 

We encourage you to explore a bit more. Are there unique searches you can build in your app that are hard to do in the interface of the site whose API you use? Something fun related to your interests?

We also encourage you to get your app running on PythonAnywhere or Google's servers (this is useful practice if you want to run your project on one one of these services), but this is not required. Still, this is a good time to connect with us in office hours work out any challenges you are having with deploying an app to a web host - as we mentioned in class, there are a bunch of small, idiosyncratic things that can go awry with getting their tools set up and configured.

# Tips
1. If you use your HW6 as a starting point, if your code calls  `flickr.photos.getInfo` on the Flickr API for many photos, running this on a server will almost certainly kill your app for taking too long to run. Try to do searches that either avoid calling that method for each photo, or focus on only on a few photos. You can adjust your call to `flickr.photos.search` to get more mdetadata back, see the `extras` parameter - https://www.flickr.com/services/api/flickr.photos.search.html
2. We followed all of the steps required for this homework in labs, including the Live Data lab in S10, the Flask Lab in S13, the PythonAnywhere & Google Cloud labs in S14, and the Flask & Forms lab in S16. You can use those slides (and corresponding code) as a guide for working with your API!
3. So that we can test this, we need your API key if your API uses one. You can check this into your private HW7 github repository, or, if you would prefer not to, you can provide it as a submission comment in Canvas. 