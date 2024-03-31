# Webshop

Webshop is a versatile Telegram bot designed to enable users to effortlessly set up and manage their own shops within the Telegram platform. With its user-friendly interface and flexible architecture, Webshop empowers users to create and customize their virtual stores with ease.

## Installation

Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install -r requirements.txt
```

## Configure

Create token using [BotFather](https://telegram.me/BotFather)

Now you need to create your telegram token and put it inside config.py.

![config](https://github.com/Unakepro/telebot/assets/68908289/5826a67c-632b-4b41-9639-518b9877a9a9)


Now the only step is to seed our database. In webshop, MongoDB is used, so make sure it's pre-installed on your pc.

```bash
python3 webshop/db/seeder.py
```

## Run

Now the only step is to run a webshop.

```bash
python3 main.py
```

## Demonstration


https://github.com/Unakepro/telebot/assets/68908289/705b4475-2c8c-4a1f-878c-422cb874fd88




## License

[MIT](https://choosealicense.com/licenses/mit/)
