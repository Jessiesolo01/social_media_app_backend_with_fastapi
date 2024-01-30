from pydantic_settings import BaseSettings

#environment variables, it is case insensitive even though in windows environment var, it is capitalized,
# pydantic will convert it on a caase insensitive basis, even environ vars in windows can be capitalized or lowercased
class Settings(BaseSettings):
    database_hostname: str#these variable names can be capitalized too, it doesnt matter
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int 

    class Config:
        env_file = ".env"

settings = Settings()