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

# Confiamos en ssokcpre/GSS-conciliacion-extranet
OAUTH2_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwCkbm4ImvCU+eSkzW8Y
f9XwyAibu7Jx+WTn69bwimHyE6JWhk3van5oaIOlOFRN8z9RMC/VCOodquo0LhS
7Wi1Q6LyhwaNiDBOcTXktrzVOcCheyWi26zGJoMT0nt59+74EJyHKRZfjrSaa8/
ey9RoCne4egpA4dXy7AeNlHxhMvW/Omdfd0007QPhjdMVVBnRiFrb4P9DSIHMRp
hx2V4nGdBqRbv7dCse9SQLy0dVIRMaPaNegBUUcnxTgg983oACC/BeY5AJll+Zv
rbUqwVsqubVZ6mND7Fkvx/bqo9PdCFbbkQY5cbJxRkzB1JimgAnGawwRCh46fE
0XCb+M03QIDAQAB
-----END PUBLIC KEY-----
"""
