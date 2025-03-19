from os.path import abspath, dirname
# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

SECRET_KEY = '123447a47f563e90fe2db0f56b1b17be62378e31b7cfd3adc776c59ca4c75e2fc512c15f69bb38307d11d5d17a41a7936789'
PROPAGATE_EXCEPTIONS = True

OAUTH2_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxI3eBpbelH0fBKi39um
LZGXPCtOH7EvPk605C0Ytzp3HrSh9Ep7y0y2exaG7mn09YYsmjtOmNx4b7wd47l
HHgJ0Y0SEM49O6cvsTX+jne8b6MKQmsU0HYGuLVoFfuOlLeGpl9h+YZkkT2LMrR
OqQDRbdcoOjljYOS++HIpduzokCdQmXPEaseYI6Fk5UI49MQcmdGgbY/+19eClO
uASVqGlbacKB91vOkGBrXlIhwpOZ/CgEOP3yh8cuPlRq4PeVYPu0/NjubFDRWyp
AGsAc7Yj1Yi8DRfelQ32EwxURpx3SqpRK9d2nEbDCEHGRfMKxwNDxlbNL/H87nt
NNDZVmSwIDAQAB
-----END PUBLIC KEY-----
"""
