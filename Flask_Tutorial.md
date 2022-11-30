## Introduction

Flask is a micro web framework built on top of Python. In terms of complexity; it sits somewhere between Django on the more complex end and Fast api on the simpler side. Flask is a good jack of all trades in the web framework space as it has the ability to scale up in complexity into something you might see in a big tech corporate, but you can also achieve great results by keeping it at its bare minimum.


## A high level view of flask

At its lowest level, a Flask instance is made up of routes. A route describes an address that the outside world can use when speaking to the api to perform some action.

Here is an example of a route using flasks route decorator  ```@app.route('/home', methods=['GET'])```

Using this route as an example we are expecting a valid response from the api when querying https://ourapi/home using a get command

The response from these routes can vary, it could be a backend response in the form of a JSON, maybe telling the front end which trades this current users has made in the past, or it could be a template response, that being the full HTML needed to render a new page. The response can vary, but the route will stay the same.


## Designing Flask for scale

If you aren't building a microservice server to handle a handful of tasks, as in what you can count on two hands, you will need to implement some method to break up the routes into logical partitions. 

Breaking up the routes like this helps you as a developer to create a system that is more easily maintained, but more importantly, a system that is easy to understand. For example; keeping all of the routes related to speaking to third party apis is a good design decision as you can ensure you keep all the code necessary to complete those kinds of tasks in one place and you wont be repeating yourself in other places.

How then do we achieve this in Flask? The answer here is the blueprint design pattern. At its core the blueprint design pattern creates a foundational instance of flask and then allows other instances of flask that could have otherwise been flask services in their own right to be appended on top of that instance in what are called, you guessed it, blueprints.

When creating routes within each blueprint you can set out a dedicated prefix for the blueprint that will provide a partition within the route structure to handle the routes within that blueprint. For example, say we have three routes in our new blueprint ```/home /users & /purchases ```

However, we had the route ```/home ``` in our foundational instance as well didn't we? Won't this cause a conflict? Yes it will!

This is where the blueprint prefix comes into play. Here we can set out a custom prefix that is added to all routes within the blueprint so you can ensure your routes are unique as well as helping the people using the api to understand the results they expect just by reading the api request.

So, here we can register a blueprint with the prefix ```/api/mynewblueprint``` using ```app.register_blueprint(new_blueprint,url_prefix='/api/mynewblueprint') ```.

Now when querying the ```/home ``` route in our new blueprint we can use ```/api/mynewblueprint/home``` and we are now pointing towards our new blueprint without any route collisions!

Congratulations, you now have a partitioned api, you can build it out as much as you would like from here.


## FAQs

### Why are the routes within a views file?

This is a holdover from the fact that the routes could return HTML templates with the relevant data injected into it, returning a "view" for the frontend to use

### What is Celery, and why is it used in Flask?

Celery is an asynchronous background task queue. Why it is important in something like an api is that one of the main SLIs (Service Level Indicators) for an api is latency. If you are trying to perform an action in your request, sending an email for example, you will be blocking the api from sending a response until that action completes. To solve for this you can hand the task off to celery to run as a background task so that it can continue to run its action after a response has been sent, thus decreasing the latency. However, a caveat here, background tasks are great for handling longer running tasks that can run in the background after a response has been sent, but sometimes you will need to sent a confirmation that the task ran successfully, for these kinds of events you will need to use a synchronous (response blocking) action instead.

### Why does the blueprint have an empty init file

This file is not necessary, it can be deleted, it is an artifact from the the blueprint having been a standalone flask instance in the past




