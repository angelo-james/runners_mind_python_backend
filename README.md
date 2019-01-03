# Runners Mind

* Clone [this repo](https://github.com/angelo-james/runners_mind_python_backend) to your local machine
* Install the dependencies with

```
pip install
```

To run app 

```
python app.py
```

Use a API development environment of your choice like postman or paw.

Hit the following endpoints
* `http://127.0.0.1:3800/api/users` (to GET all users)

To create a user make a POST request hitting this endpoint `http://127.0.0.1:3800/api/users`
* In the request pass a json body

```
{
	"name": "toad",
	"email": "toad@email.com",
	"password": "password"
}
```

To make a DELETE request hit this endpoint `http://127.0.0.1:3800/api/users`
* Make sure to pass a exsisting users id within the params