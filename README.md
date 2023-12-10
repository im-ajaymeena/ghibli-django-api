
# Django ghibli API

## Overview
- This API acts as a proxy to `https://ghibli.rest/`.
- The data from `https://ghibli.rest/` is saved in database every 1 minute using a custom command facilitated by the Django-cron package.
- The logs for the cron-job execution can be viewed on the admin page.


## Setting Up and Running the Project
To set up and run this project locally, follow these steps:

### Prerequisites
- Ensure you have Docker installed on your machine.

### Running the Project
- To start the project, simply run the following command in your terminal:
  ```bash
  docker-compose up
  ```

## API Endpoint
**URL**: `http://localhost:8080/films/`

## Authentication
This API requires an API key for access. Use the following header for authentication:
- **Header Key**: `X-SECRET-KEY` & **Value**: `h2R6f8Gp#QxYsJt`

- There are extensions such as "Modify Headers for Google Chrome," for making custom headers for all requests. 
- Note: The API key is set using the environment variable `ghiblikey` in the Docker-compose file.


## Response Structure
When you make a request to the endpoint, the API returns a JSON response with the following structure:

```json
{
    "id": "<film_id>",
    "actors": [
        {
            "id": "<actor_id>",
            "name": "<actor_name>",
            "species": "<species_type>",
            "url": "<actor_url>"
        },
        // More actors...
    ],
    "title": "<film_title>",
    "original_title": "<original_title>",
    "original_title_romanised": "<romanised_title>",
    "image": "<image_url>",
    "movie_banner": "<banner_url>",
    "description": "<film_description>",
    "director": "<director_name>",
    "producer": "<producer_name>",
    "release_date": "<release_year>",
    "running_time": "<duration_in_minutes>",
    "rt_score": "<rotten_tomatoes_score>",
    "url": "<film_url>",
    "species": [
        "<species_id>"
    ],
    "locations": [],
    "vehicles": [
        "<vehicle_id>"
    ]
}
```

## Example Request

```bash
curl -H "X-SECRET-KEY: h2R6f8Gp#QxYsJt" http://localhost:8080/films/
```


