# Lexicard
A website that generates flashcards by providing documents.

## Contributors

Agosto, Fredierick [@Poemeu](https://github.com/Poemeu)

Apas, John Clyde [@Glitch-1010](https://github.com/Glitch-1010)

Caracena, Geralyn [@alyn13](https://github.com/alyn13)

Cellan, Kate Aubrey [@DaijobuDes](https://github.com/DaijobuDes)

Genegabuas, Seejee [@densentsu124](https://github.com/densentsu124)

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

## Deploying the server

Install nginx on linux.

```sh
$ sudo apt install nginx
```

Inside `configuration` folder, configure `flashcard.conf`, change fields to where you need to place them.

Add SSL server certificates in order to enable HTTPS mode. (HTTP mode, plain/text data exchange is NOT recommended.)

For the `run_server` file, edit both `--user` and `--group` to your desired username and execute `chmod +x ./configuration/run_server` while being in the root of the project.

Run with `./configuration/run_server`.

