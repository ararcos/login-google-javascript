# Office Desk Reservation Backend

## Setup environment

### Requirements

- Python (You can install it by following the steps in this [link](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-22-04))
- Poetry (You can install it by following the steps in this [link](https://python-poetry.org/docs/master#installing-with-the-official-installer))
- Make (You'll have to search it how to install for your operative system)
- pyenv (You can install it by following the steps in this [link](https://github.com/pyenv/pyenv-installer))[OPTIONAL]

This step is optional, if you want to work with a simple Python version management tool (pyenv), if you don't, just install Python 3.9.0 version. Remember before working with pyenv, make sure you have the necessary dependencies for your operating system. Here a [link](https://github.com/pyenv/pyenv/wiki/Common-build-problems) that can help you.

In this project we'll use Python 3.9, so you have to install it by using the next command.(If you choose work with pyenv)

```
pyenv install 3.9.0
```
In the project directory, the following command is executed to indicate which version of Python will be used in that directory, in this case 3.9.0 version. (If you choose work with pyenv)

```
pyenv local 3.9.0
```

Then, you must indicate Poetry which version of Python will be used to configure the virtual environment.

```
poetry env use 3.9.0
```

After to do the last step, execute  `make install` command which will create the virtual environment and download the project dependencies. 

To activate the virtual environment and execute instructions within it, you must run `poetry shell`.

You can also execute commands directly within the virtual environment by typing `poetry run` followed by the instruction in the command line.

### Git Hooks
Please install the git hooks by running

 ```
make hooks
```

It includes the pre-commit (wrong branch name validation), post_checkout (wrong branch name validation), commit-msg (valid message validation) and pre-push (lint, test and branch validation before push).


### Set black formatter
first we activate the python virtual environment, with the command:
`source ./.venv/bin/activate`
make sure all dependencies are installed whit:
`poetry install`
finally set black as your default code formatter in your editor, here is an example in vsCode.

![config vscode](https://i.imgur.com/ZqEWOvo.png)

### Add variables

In the root directory /Office-Desk-Reservation-Backend create a file .env with these value

    FIREBASE_TYPE=XXX
    FIREBASE_PROJECT_ID=XXX
    FIREBASE_PRIVATE_KEY=XXX
    FIREBASE_CLIENT_EMAIL=XXX
    FIREBASE_TOKEN_URI=XXX

Ask your teach lead for the credentials.

## How to contribute to the project

Clone the repository and from the `dev` branch create a new branch for each new task. You must follow the recommended branch name like below: 

If your name is Carlos Rodriguez

```
    CR/OFI-<number_ticket>-<title_ticket>
```
Where "CR" are the initials of your name. 

E.G: 

```
    CR/OFI-250-update-readme
```
## Commit the message: 

- The project use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) standards.
- The message should be in the following format: 
    ``` 
    feat: OFI-219 modify readme 
    fix: OFI-02 fix function get_example.py
    ```
- Commit types:
    - `fix` : hotfix or something that was fixed because of a bug
    - `feat` : refers to a feature, a new requirement
    - `test` : refers to test code, e.g. unit testing, integration testing
    - `refactor` : refers something was modified in the code, e.g. naming

## Create the Pull Request (PR)

- Submit the feature (`git push`) and create a PR to `dev` branch.
- Explain what has been done, what has been fixed or if you have created a new feature.
- Include reviewers in the PR.

## Architecture
The application follows a DDD approach with a hexagonal clean architecture. BIG WORDS!, what does it mean? it means the following:

We have a directory for each domain entity (i.e. Office, Parking etc)
Inside each entity directory we have other 3 directories (application, domain and infrastructure)
I'll leave this drawing to understand how these three folders work and what logic should be included in these directories.

![Image about diagram architecture](https://wata.es/wp-content/uploads/2021/05/diagrama-arquitectura-hexagonal-wata-factory-1024x796.png)

## How to choose the status codes responses
Instead of using an int status code, now you will have to use the name of the status itself, for that you can find information in the following [documentation](https://docs.python.org/3/library/http.html).

## Secrets change
In case you want to change or add a secret, please run the following command:
    ``` 
    sops .env.sops.stg.json
    ```
Please make sure you have the AWS credentials of the project account so you can be able to modify the file.
