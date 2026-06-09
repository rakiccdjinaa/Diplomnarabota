class Config:

    SQLALCHEMY_DATABASE_URI = (

        "mysql+pymysql://root:constellations21@localhost/cdss_system"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "super_secret_key"