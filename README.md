# Circular Fashion

## Setup

### Assumptions

It's assumed that you have the following installed:
- Docker/Docker Compose
- Python (tested with 3.8, others might work)

 
### Installation
- Once you have docker installed, we just need to build the containers and start them up. The containers 
are managed with docker-compose. The containers managed include instances of Nginx, Postgres and this 
Django application.

- Start the application with the following docker-compose command:
    ```bash
    docker-compose up --build -d
    ```
  The `--build` flag helps to build the containers if they have not been built before or some changes
  have been made to configurations and dependencies since the last time they were built.
  Then the `-d` flag runs the containers in detached mode (they don't block your terminal).
  
- To start the application, you may want to run migrations first by executing:
    ```bash
    docker-compose exec web python manage.py migrate
    ```
 
- You should be able to access the application on the host machine at port `80`. If you wish to run it on
another port, you should change the configurations on the `docker-compose.yml` and choose a convenient 
port for the Nginx server to interface with the host machine.


### Tests
There are just few tests in there which of course can be improved on and added to boost confidence 
in the workability of the API service.


### APIs Endpoint
There are currently only two endpoints in the application which are 
`/materials/<int:material_id>/attributes/` : which returns the attributes (Cotton Percentage, Polyester 
and so on, depending on your custom attributes) and also `/materials/recyclers/` which return all the data 
based on the recyclers, in other words, this endpoint returns a list of recyclers and the qualities stated.
Example of the payload returned by this endpoint is:

```json
[
    {
        "id": 1,
        "name": "Recycler 1",
        "qualities": [
            {
                "id": 1,
                "title": "Quality 1",
                "min_count": -1,
                "material": {
                    "id": 1,
                    "name": "Material 1",
                    "attributes": "http://localhost:8000/api/materials/1/attributes/",
                    "attributes_count": 18
                },
                "condition": "(ATTR_POLYESTER == 0.7) and (ATTR_COTTON == 0.3) and (ATTR_DYE_METHOD == OPT_TOP_DYED)",
                "operations": [
                    {
                        "operands": [
                            "ATTR_POLYESTER",
                            0.7
                        ],
                        "operator": "=="
                    },
                    {
                        "operands": [
                            "ATTR_COTTON",
                            0.3
                        ],
                        "operator": "=="
                    },
                    {
                        "operands": [
                            "ATTR_DYE_METHOD",
                            "OPT_TOP_DYED"
                        ],
                        "operator": "=="
                    }
                ],
                "passed": true
            }
        ]
    }
]
``` 

while the initial endpoint (material attributes) return data like this:

```json
[
    {
        "id": 1,
        "attribute": {
            "id": 2,
            "name": "Cotton",
            "placeholder": "COTTON",
            "category": {
                "id": 1,
                "name": "Composition"
            }
        },
        "value_type": "p",
        "choice": null,
        "percentage": "30.00"
    },
    {
        "id": 13,
        "attribute": {
            "id": 14,
            "name": "Other Cellulosics",
            "placeholder": "OTHER_CELLULOSICS",
            "category": {
                "id": 1,
                "name": "Composition"
            }
        },
        "value_type": "p",
        "choice": null,
        "percentage": "0.00"
    },
    {
        "id": 14,
        "attribute": {
            "id": 15,
            "name": "Others",
            "placeholder": "OTHERS",
            "category": {
                "id": 1,
                "name": "Composition"
            }
        },
        "value_type": "p",
        "choice": null,
        "percentage": "0.00"
    },
    {
        "id": 18,
        "attribute": {
            "id": 22,
            "name": "Dye Stuff",
            "placeholder": "DYE_STUFF",
            "category": {
                "id": 20,
                "name": "Dyes"
            }
        },
        "value_type": "c",
        "choice": {
            "id": 18,
            "name": "Reactive Dyes",
            "placeholder": "REACTIVE_DYES"
        },
        "percentage": null
    },
    {
        "id": 17,
        "attribute": {
            "id": 21,
            "name": "Dye Method",
            "placeholder": "DYE_METHOD",
            "category": {
                "id": 20,
                "name": "Dyes"
            }
        },
        "value_type": "c",
        "choice": {
            "id": 14,
            "name": "Top Dyed",
            "placeholder": "TOP_DYED"
        },
        "percentage": null
    },
    {
        "id": 16,
        "attribute": {
            "id": 19,
            "name": "Light/Dark",
            "placeholder": "LIGHTDARK",
            "category": {
                "id": 18,
                "name": "Colour Shade"
            }
        },
        "value_type": "c",
        "choice": {
            "id": 8,
            "name": "Light",
            "placeholder": "LIGHT"
        },
        "percentage": null
    },
    {
        "id": 15,
        "attribute": {
            "id": 17,
            "name": "Type",
            "placeholder": "TYPE",
            "category": {
                "id": 16,
                "name": "Fabric Construction"
            }
        },
        "value_type": "c",
        "choice": {
            "id": 3,
            "name": "Thread",
            "placeholder": "THREAD"
        },
        "percentage": null
    }
]
```
