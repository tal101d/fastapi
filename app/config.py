from pydantic_settings import BaseSettings


class Settings(BaseSettings): # with this inheritance we create enviormnets variables. they suppose to be capitalized but pydantic take cate of it
                              # When we create an instance of the Setting class Pydantic will check id this evio variables are exist in the system
                              # if they do, it will assign them acordinglly to the names and we can access them.
    database_hostname: str
    database_port: str        # its a str and not int because we will use it in a URL path.(we can take it as an int to see if its valid but not nessecery) 
    database_password: str
    database_name: str
    database_username: str
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int
    

settings = Settings(_env_file='.env')
