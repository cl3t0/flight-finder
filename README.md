# Flight Finder

This project helps you find the best airport and day to travel based on the lowest price. It uses the Poetry package manager for managing dependencies.

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