# google_api_by_python
This is repository for using Google API by Python

## Before use
- Set up a project on Google Cloud Platform:  
    - Create a project in the Google Cloud Console.  
    - Enable the Gmail API and Drive API.
    - Create an OAuth 2.0 client ID and obtain a client ID and client secret.
    - Download the credentials into this system (./data/confidential/client_secret.json).

- Install Python libraries:
    - google-auth
    - google-auth-oauthlib
    - google-auth-httplib2
    - google-api-python-client
    - google-api-core
    - googleapis-common-protos

 ## How to use
1. You can install python libraries by this command:
    ```bash
    make install
    ```
2. You can run this system by this command:
    ```bash
    make run
    ```
    