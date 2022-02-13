# 69LibAPI Documentation

69Lib is a library/book storage management API, it help both users and administrators perform basic CRUD operations on a library database

## Installation

Follow this process only if you want to use the API locally


### Dependencies

First clone the repo or download it as a zip

Once done you will need [python](https://python.org) 3.10.0 or higher

And the package manager [pip](https://pip.pypa.io/en/stable/) or [pip3](https://pip.pypa.io/en/stable/)

We recomment using a [virtual environment](https://docs.python.org/3/library/venv.html)

By running

```bash
pip -r requirements.txt
or
pip3 -r requirements.txt
```
You will install the required modules inside the *requirements.txt* file

The key dependencies for this project are:
* [Flask](https://flask.com)
* [SQLAlchemy](https://sqlalchemy.com)

Once you are done go ahead and run

__For MacOs or Linux__ 
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

```

__For Windows__ 
```bash
set FLASK_APP=<file_name.py>
set FLASK_ENV=development
flask run

```  

In certain cases you might need to add
```bash
$env:FLASK_APP = "<file_name.py>"
```
## Usage

The API is based on a one to many relationship between categories and books. Thus we have the following routes

We assume all routes are preceded by the API's url which is __https://library-69-api.herokuapp.com/__

 __GET__ ALL BOOKS


```
~/books       
```

This route like most of the other ones send back an array of 3 elements:
* A "Success" field which is equal to True if the request is approved
* A "books" field which contains every book in the database in a json format
* A "total" field which is basically the number of books in the library

 __GET__ A BOOK BY ITS ID

```
~/books/<booksId>
```
Returns two fiels: 
* "Success" 
* And "book" which is the requested book

 __GET__ A CATEGORY BY ITS ID

```
~/categories/<categoryId>
```

Returns two fiels: 
* "Success" 
* And "category" which is the requested category

 __GET__ ALL CATEGORIES
```
~/categories
```
Returns three fiels: 
* "Success" 
* "categories" which is an array of all categories in json format
* "total" the number of categories in the library

 __GET__ ALL BOOKS FROM A CATEGORY
```
~/categories/<categoryId>/books
```
Returns four fiels: 
* "Success" 
* "books" which is an array of all books in the requested category
* "total" the number of books returned
* "label" the requested category's label

 __DELETE__ A BOOK/CATEGORY

These routes will only respond to *DELETE* requests
```
~/categories/<categoryId>      or
~/books/<bookId>
```
Returns twofiels: 
* "Success" 
* "deleted book/category" a json format of the item you just deleted

 __UPDATE__ A BOOK/CATEGORY

These routes will only respond to *PATCH* or *PUT* requests
```
~/categories/<categoryId>..params..      or
~/books/<bookId>..params
```

For example we want to update the category (1, "Culinar) to (1, "Tech review")

The route would then be 
```
~/categories1?label=Tech%20review
```
Note that you can just update the category's label as it is it's only mutable attribute(the other one being the id), the books have many more fields to update .

Returns twofiels: 
* "Success" 
* "updated book/category" a json format of the item you just updated


## Error handling

You can come accross three types of error while using the 69LibAPI
### Error 400: Bad Request
If you get this error then you might want to double check your request, look for possible typos or missing params when updating

### Error 405: Method not allowed

The method you are using to access the route is not defined for that route, you might want to double check the route or the methods

### Error 404: Not found

The ressource you are looking for is either not on the server anymore or have never been on it

### Error 500: Internal Server

Here you are not the one to blame, this means we have a problem on our server, this is where you become the hero


## Contributing
Pull requests are welcome. If you think you can improve in any way the API, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Made with ♥ by [TheWisePigeon](https://github.com/TheWisePigeon)
