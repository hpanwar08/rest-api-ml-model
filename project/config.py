class BaseConfig:
    TESTING = False
    SECRET_KEY = "kajsv7r9wy8f98y98r928#%GFDU%$2198fy98wye"


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
