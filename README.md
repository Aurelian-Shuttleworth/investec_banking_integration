# investec_banking_integration

## To use the library:
1. import investec
2. create an InvestecClient, supply the class construction with the client_id and client_secret
3. Note the client_id and client_secret is not persisted in the class instance and imediately used to build a basic
 base64 encrypted token. The token created will then be used to generate an access_token through use of the client. 
 This is done behind the scenes if the timer has expired and only if a new request is attempted.
 
Code will look as follows:

`
bank_client = InvestecClient(client_id, client_secret)
method = "accounts" # accounts, account_transactions, account_balance
bank_client.access_bank(method, accountId=account_id)   # optional kwargs include:  fromDate, toDate, transactionType
`

## Setup a virtual environment:

## How to publish to pip:
1. You require the following installations, run the below commands:

$`python -m pip install --upgrade pip setuptools wheel`

$`python -m pip install tqdm`

$`pip install twine`

2. Following the above installations do the following:

$`python3 setup.py sdist bdist_wheel`

$`python -m twine upload dist/*`

3. When doing a new release, remember to increment the version in the setup.