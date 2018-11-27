class ParentConfig:
    """ Parent configurations """
    DEBUG = False
    TESTING = False
    JWT_ACCESS_TOKEN_EXPIRES = False

class DevelopmentConfig(ParentConfig):
    """ Development config """
    ENV = 'development'
    DATABASE = 'storemanager'
    DEBUG = True
    TESTING = False

class TestingConfig(ParentConfig):
    """ Testing environment """
    ENV = 'testing'
    DATABASE = 'storemanager_test_db'
    DEBUG = True
    TESTING = True


class ProductionConfig(ParentConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    HOST = 'ec2-54-83-27-162.compute-1.amazonaws.com'
    DATABASE = 'dcojjie21dvmis'
    USER = 'sejawvmmzwabhv'
    PASSWORD = '26c76331cf6695b3226de7db2d6405f757329228c9e84b858a29847e030d6044'
   
app_config = dict(
    development = DevelopmentConfig,
    testing = TestingConfig,
    production = ProductionConfig
)