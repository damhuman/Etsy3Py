# Etsy3Py
Client for Etsy API v3

## Installation
You can install etsy3py using pip:

``` python
pip install etsy3py
```

## Requirements
Python 3.6 or higher.

# Etsy API
This is a Python client for the Etsy API. 
The client makes it easy to interact with the Etsy API and perform operations on a user's behalf.

## Usage
To use the EtsyApi class, you will need to obtain an access token from the Etsy API.

``` python
from etsy3py.v3 import EtsyApi

access_token = "YOUR_ACCESS_TOKEN"
client_id = "YOUR_CLIENT_ID"

etsy_api = EtsyApi(access_token=access_token, client_id=client_id)

listing_id = 12345
listing = etsy_api.get_listing(listing_id)
```

### Authentication
The EtsyApi class uses OAuth 2.0 authentication. You will need to obtain an access token from the Etsy API 
before using the client. You can obtain an access token by following the
instructions in the Etsy API documentation.

### Rate Limiting
The Etsy API has a rate limiting policy that limits the number of requests that can be made in a given time period.



# Authentication step-by-step
`EtsyOAuthClient` is a Python class that provides an authentication client for the Etsy marketplace API, 
allowing users to connect to the API using OAuth2 authentication.

## Usage
Here is an example of how to use the EtsyOAuthClient to obtain an access token from the Etsy API.

``` python
from etsy3py.oauth import EtsyOAuthClient
```

Replace these with your own values from the Etsy Developer Console

``` python
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri' 
scope = ['your_scope_1', 'your_scope_2', ...]
```

Create an instance of the EtsyOAuthClient

``` python
client = EtsyOAuthClient(client_id, client_secret, redirect_uri, scope)
```

Get the authorization URL

``` python
authorization_url, state = client.authorization_url()
```

Redirect the user to the authorization URL to grant access. Once the user has granted access, get the authorization code and use it to obtain an access token

``` python
authorization_code = 'the_authorization_code'
access_token = client.fetch_token(authorization_code)
```

You can now use the access token to make requests to the Etsy API

# Refresh token

The `refresh_token` method of the `EtsyOAuthClient` class requests a new access token from the authorization server using a refresh token.

### Parameters

`refresh_token` (required): The refresh token used to obtain a new access token.

### Return Value

The `refresh_token` method returns a dictionary containing the new access token and any additional data returned by the authorization server.

## Usage

Replace these with your own values from the Etsy Developer Console

``` python
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# create an instance of the EtsyOAuthClient

client = EtsyOAuthClient(client_id, client_secret)

# if the access token expires, you can use the refresh token to obtain a new access token and additional data 

new_access_token = client.refresh_token(refresh_token)
```

#### This package is licensed under the MIT License.