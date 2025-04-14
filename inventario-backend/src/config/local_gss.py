# config/local.py

from . import default

APP_ENV = default.APP_ENV_LOCAL
SQLALCHEMY_DATABASE_URI = 'sqlite:///authz.sqlite'

# Confiamos en los tokens JWT de ssokc2pre/GSS
OAUTH2_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwCkbm4ImvCU+eSkzW8Y
f9XwyAibu7Jx+WTn69bwimHyE6JWhk3van5oaIOlOFRN8z9RMC/VCOodquo0LhS
7Wi1Q6LyhwaNiDBOcTXktrzVOcCheyWi26zGJoMT0nt59+74EJyHKRZfjrSaa8/
ey9RoCne4egpA4dXy7AeNlHxhMvW/Omdfd0007QPhjdMVVBnRiFrb4P9DSIHMRp
hx2V4nGdBqRbv7dCse9SQLy0dVIRMaPaNegBUUcnxTgg983oACC/BeY5AJll+Zv
rbUqwVsqubVZ6mND7Fkvx/bqo9PdCFbbkQY5cbJxRkzB1JimgAnGawwRCh46fE0
XCb+M03QIDAQAB
-----END PUBLIC KEY-----
"""
