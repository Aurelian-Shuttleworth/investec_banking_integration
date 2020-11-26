# investec_banking_integration

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