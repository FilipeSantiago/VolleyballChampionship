from __future__ import annotations
from typing import Optional
import os


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instance: Optional[InitConfig] = None

    def __call__(self) -> InitConfig:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class InitConfig(metaclass=SingletonMeta):

    def __init__(self):
        self.config = {
            "port": os.getenv("APP_PORT", 5000),
            "database_config": {
                "service": os.getenv("DATABASE_SERVICE", "postgresql"),
                "ip": os.getenv("DATABASE_HOST", "localhost"),
                "port": os.getenv("DATABASE_PORT", "5432"),
                "user": os.getenv("DATABASE_USER"),
                "pass": os.getenv("DATABASE_PASSWORD"),
                "database": os.getenv("DATABASE_NAME", "volley_championship"),
                "schema": os.getenv("DATABASE_SCHEMA", "public")
            }
        }

        print(self.config)

    def get_config(self):
        return self.config
