# PesaPal API Integration

### By Joanne Gitari 

## Description
This API allows you to get the Pesapal iframe URL by consuming the Pesapal API v3.0. It authenticates using JWT Tokens.

## Setup Requirements

* Git
* Github
* Python
* FastAPI
* PesaPal API v3.0

## Setup Installation

* Copy this repository's link 🌐
```
https://github.com/joeygitari/pesapal-api-integration
```
* Clone it to your local machine 💻
```
$ git clone https://github.com/joeygitari/pesapal-api-integration.git
```
* Open your terminal and navigate to the directory of the project 📁
```
$ cd pesapal-api-integration
```
* Follow the documentation below 📑
```
https://developer.pesapal.com/how-to-integrate/api-30-json/api-reference
```
* Run the following commands to install the required dependencies.
```
$ pip install -r requirements.txt
```
* Set up environment variables:
Create a .env file in the project directory and add the following variables
```
CONSUMER_KEY=your-pesapal-consumer-key
CONSUMER_SECRET=your-pesapal-consumer-secret
```

## Usage
* Start the FastAPI server
```
$ uvicorn main:app --reload
```
* Open your web browser and navigate to http://localhost:8000 to access the application.

* Authenticate and obtain an access token:
Send a POST request to /login with the following request body:
```
{
  "username": "test",
  "password": "test"
}
```
This will return an access token that you can use for further requests.
* Retrieve an access token from Pesapal:
Send a GET request to / to retrieve an access token from Pesapal. The response will include the access token if the request is successful.

* Register an IPN URL:
Send a GET request to /ipnUrl to register an IPN URL with Pesapal. This will return the registered IPN URL and other relevant information.

* Submit a payment order:
Send a GET request to /submitOrder to submit a payment order to Pesapal. This endpoint requires authentication with a valid access token obtained in step 3. The response will include the status of the submitted order.

## Configuration
* The application uses environment variables for configuration. 
You can set these variables in the .env file as mentioned in the installation steps. 
The available configuration options are:
```
CONSUMER_KEY: Your Pesapal API consumer key.
CONSUMER_SECRET: Your Pesapal API consumer secret.
```

## Security 
The application uses JSON Web Tokens (JWT) for authentication. 
The /login endpoint generates an access token, which must be included in the Authorization header as a bearer token for authenticated requests.

## Development
To contribute to the project or make modifications, follow these guidelines:

* Fork the repository and clone it to your local machine.
* Create a new branch for your changes: git checkout -b my-new-branch
* Make the necessary modifications and test your changes.
* Commit your changes: git commit -am 'Add some feature'
* Push to the branch: git push origin my-new-branch
* Create a new pull request and describe your changes in detail.

## Known bugs
There are no known bugs at the moment. 😎

## Support and contact details

For any contributions contact:
* Email : jgitaridev@gmail.com 
* Phone : 0706804187 

# License 

Copyright ©️ 2023 Joanne Gitari

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
