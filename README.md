# Flight Finder

This project helps you find the best airport and day to travel based on the lowest price.

## Running with Docker

After cloning the repository, you can build a docker image using the following command:

```
make docker-build
```

Run the project running:

```
make docker-run
```

and a CLI will appear.

## Running without Docker

After cloning the repository, you will need all the requirements:

- Python 3.10.9 (You can use [pyenv](https://github.com/pyenv/pyenv) to install a specific Python version)
- Poetry (Read how to install it by clicking [here](https://python-poetry.org/docs/#installation))


Install the project dependencies using Poetry:

```
poetry install
```

Execute the CLI using the command:

```
make cli
```

## Usage

Here's an example of CLI interaction:

```
Enter a new airport (Enter an empty string to stop): JFK
Enter a new airport (Enter an empty string to stop): GRU
Enter a new airport (Enter an empty string to stop): PHX
Enter a new airport (Enter an empty string to stop): 
Enter the lower bound date: 2023-03-01
Enter the upper bound date: 2023-08-01
Enter the center airports limit: 15
Enter how much flight suggestions do you want: 10
```

Most of the arguments are self-explanatory except one: center airports limit.
center_airports_limit: This is an argument that specifies the number of center airports to consider for the search. The search precision and running time will both decrease if this number decreases and vice-versa.

## Context and Challenges

This project is part of the selection process that I'm attending right now. Here I'm going to talk about how I figured out how to solve the initial problem.

The initial problem was:

`
Given a list of cities where we live and a range of dates please use a flight pricing API to determine what would be the cheapest city to fly to a company offsite.
`

First of all, I need to choose an API to use as a data source. Wasting some time I found the Amadeus website. The free tier of it supports 2000 requests per month and I think it’s enough for what we are trying to do. So I registered, read the [documentation](https://developers.amadeus.com/self-service/category/air/api-doc/flight-offers-search/api-reference), and started coding.

I created my project using [Poetry](https://python-poetry.org/), created a GitHub repository, and installed mypy to use static typing and pytest to make my tests. My first test was an integration test to see if everything connects as it should.

![ alt text for screen readers](/assets/firstintegtest.png)

After writing enough code to make this test work we can make a mocked version of the API to use in unit tests.

I found on the internet an [SQLite table](https://www.partow.net/miscellaneous/airportdatabase/index.html#Downloads) describing all airports with coordinates. I’m going to use it to estimate the midpoint of all related airports and reduce API calls which allow us to stay on the free tier. I made an interface and tests for it too.

![ alt text for screen readers](/assets/secondintegtest.png)

As before, now we can make a mocked version of it too.

I’m using the [circular mean](https://en.wikipedia.org/wiki/Circular_mean) to calculate the midpoint of a collection of coordinates in the globe, which minimizes geodesic distance. The implementation of this pure function can be found at flight_finder/mathematics.py and this file is fully covered by tests too.
Mocking the API and the airport's table interface allows us to implement and write tests to our main function: find_best_airports_and_days which is at flight_finder/find.py.

![ alt text for screen readers](/assets/findtest.png)

The idea is this function returns the best airports, on which date, and for which price. After implementing it, everything works nicely with mocked API and mocked airports table.

I got some errors and needed to start from the beginning a significant quantity of times so I thought a good idea could be to cache the API output locally. It can speed things up and save some API calls. So I implemented the SqliteCacher which implements AbstractCacher (It exists to allow us to change the caching strategy in the future). After it, I created the CachingWrapper which receives an API and some caching strategy and implements the same interface of an API. I wrote tests for everything I mentioned. Using this wrapper looks like this:

Before:


```python
client = AmadeusApi(key, secret, url)
```

After:


```python
cacher = SqliteCacher("cache.db")
client = CachingWrapper(AmadeusApi(key, secret, url), cacher)
```

With everything done and working, I documented every function, created the Dockerfile, created the Makefile, created the CI pipeline with GitHub Actions, wrote this README and adjusted every detail to work as I wanted. That's it.de