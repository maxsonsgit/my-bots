from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admins_id: list[int]


@dataclass
class MongoDB:
    db_uri: str


@dataclass
class Config:
    tg_bot: TgBot
    mongo_db: MongoDB


def load_data(path: str | None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"), admins_id=list(map(int, env.list("ADMINS_ID")))
        ),
        mongo_db=(MongoDB(db_uri=env("DB_URI"))),
    )
