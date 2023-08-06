"""
Json responses should include the following keys:
status: success or error
code: status code number
messages: helpful message from the api
results: dictionary with the results of the previous request
        based on the object type as key,
        ex. user = dict of user data
        users = list of dicts containing each users data.
        May also include pagination data.

example response json:
{
    "status": "success",
    "code": 200,
    "messages": ['User was created'],
    "results": {
        "user": {
            "uuid": "some_uuid",
            "first_name": "John",
            "last_name": "Doe",
            "email": "JDoe@email.com"
        }
    }
}
"""
