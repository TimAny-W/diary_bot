from dataclasses import dataclass
import configparser


@dataclass
class Bot:
    BOT_TOKEN: str


@dataclass
class Config:
    tg_bot: Bot


def load_config(path: str) -> Config:
    """Read and return config"""
    config = configparser.ConfigParser()
    config.read(path)

    settings = config['BOT_CONFIG']

    return Config(tg_bot=Bot(BOT_TOKEN=settings['BOT_TOKEN']))

