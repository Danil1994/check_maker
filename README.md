Задача:
Розробити REST API для створення та перегляду чеків з реєстрацією та авторизацією користувачів.

# Check_maker

REST API for creating and viewing checks with user registration and authorization.

## Install

1. Clone repo:
   --Clone with SSH `git clone https://github.com/Danil1994/check_maker.git`
   --Clone with HTTPS `git clone git@github.com:Danil1994/check_maker.git`

2. Go to your project folder: `path/to/the/folder`.
3. Load your .env file like .env.example. And provide all the required information (passwords, secret keys etc).
4. Install requirements.txt: `pip install -r requirements.txt`.
5. Configure your connection parameters database.py -> SQLALCHEMY_DATABASE_URL=...

## Run

1. Run server: `uvicorn main_app.main:app --reload`
2. Go to link `http://127.0.0.1:8000/docs#/` in your browser.

## Using

* Registration and Confirmation.

`/register/{
"username": "string",
"password": "string"
}`
accepts 2 parameters for user registration

`/token/{
"username": "string",
"password": "string"
}`
issues an access token to registered users

* Creating Sales Receipt /check/


  Authorized users should be allowed to create sales receipts for goods. Each receipt should contain the following
  information: information about the items, their quantity, price, and any additional data (if necessary). For each
  receipt, an identifier, creation date, and the identifier of the user who created the receipt should be saved.

  The method should accept the following request body:
    * List of items
    * Name
    * Price per unit
    * Quantity of the item or its weight
    * Information about payment for the purchase of goods
    * Type (cash/card)
    * Amount

      In response, the method should return the additionally calculated cost for each item in the receipt, the total
      amount of the receipt, and the amount of change to be given to the customer.
      For example, the request body may look like this:
    * ```
      `{
      "products": [
      {
      "name": string,
      "price": decimal,
      "quantity": int,
      },
      ...
      ],
      "payment": {
      "type": "cash" / "cashless",
      "amount": decimal,
      },
      }
      ```
     
      response: 
  ```{
      "id": ...,
      "products": [
      {
      "name": string,
      "price": decimal,
      "quantity": decimal,
      "total": decimal,
      }
      ],
      "payment": {
      "type": "cash" / "cashless",
      "amount": decimal,
      },
      "total": decimal,
      "rest": decimal,
      "created_at": datetime,
      }
   ```


* Get check`/check/`

  After successful authorization, users are given the opportunity to view their list of checks. Each check contains
  information such as an identifier, date of creation, total amount and other information that characterizes it.

  In addition, users can retrieve information about a specific check by its unique identifier, which they received when
  creating the check.

  In order to conveniently search for specific checks, users are given the opportunity to apply various filters.
  Examples
  of such filters may include:

  Filtering by check creation date (for example, displaying checks created within the last month).
  Filtering by the total amount of the receipt (for example, showing only receipts with purchases above a certain
  amount).
  Filtering by payment type (for example, displaying checks paid in cash).
  API request parameters can be used to implement these filters.
  -`created_before`  all checks wich created before current date example "09.05.2024 19:43"
    - `created_after`  all checks wich created after current date example "09.05.2024 19:43"
    - `max_sum` all checks with the specified amount or less
    - `min_sum` all checks with the specified amount or more
    - `type_payment` selects all checks with the specified payment type cash/cashless
    - `limit(query) Default value : 10` the number of entries per page
    - `page (query) Default value : 1` page number to display
    - `offset` number of records to skip

  In addition, pagination is provided for easy navigation of search results. The user can specify the number of entries
  on
  the page, the number of the current page or the number of the first entries to be skipped.

* Get check by ID `/check/{check_id}`

  along the specified route, you can receive a specific check for the specified ID

* Get text check `/text_check/{check_id}`

  you can view the text version of a specific check along the specified route. You can optionally set the width of the
  check period


