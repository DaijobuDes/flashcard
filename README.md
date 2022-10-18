# Lexicard
A website that generates flashcards by providing documents.

## Setup
1. Install python. Stable version [3.8.9](https://www.python.org/downloads/release/python-389/) and [Git](https://git-scm.com/downloads).

2. Clone this repository by opening a command prompt/terminal.
```bash
$ git clone https://github.com/DaijobuDes/flashcard
```

3. Creation of the virtual environment.
```sh
$ cd flashcard
$ py -m venv .
```

4. Activate the virtual environment.

On Windows Powershell:
```ps
PS> Set-ExecutionPolicy Unrestricted
PS> Scripts\activate
```

On Windows Command Prompt:
```cmd
> Scripts\activate.bat
```

On Linux/Mac: (Make sure you have **python3-pip** installed)
```sh
$ source bin/activate
```

5. Install requirements
```sh
$ pip3 install -r requirements.txt
```

6. Run the server
```sh
$ py ./manage.py runserver
```

