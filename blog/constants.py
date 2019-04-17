import os

# constants for r2dto serializer validators
EMAIL_PATTERN = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
USERNAME_PATTERN = r'([a-zA-Z0-9]{,})$'

BLOG_TEST = os.environ.get('BLOG_TEST', '').lower() == 'true'

# run blog database migrations on application start
BLOG_RUN_MIGRATIONS = os.environ.get('BLOG_RUN_MIGRATIONS', '').lower() == 'true'

# all blog content will be cnrypted before entering the database
# likewise all blog content must be decoded
BLOG_CONTENT_KEY = os.environ.get('BLOG_CONTENT_KEY', 'mWmYSBcSzfhGuLCRvqc3A9xK')

# blog api specifications
BLOG_HOST = os.environ.get('BLOG_HOST', '0.0.0.0')
BLOG_PORT = int(os.environ.get('BLOG_PORT', '8000'))
BLOG_WORKERS = int(os.environ.get('BLOG_WORKERS', '1'))

# blog redis specifications
BLOG_REDIS_HOST = os.environ.get('BLOG_REDIS_HOST', '127.0.0.1')
BLOG_REDIS_PORT = int(os.environ.get('BLOG_REDIS_PORT', '6379'))

# blog mongodb specifications
BLOG_DB_HOST = os.environ.get('BLOG_DB_HOST', '127.0.0.1')
BLOG_DB_PORT = os.environ.get('BLOG_DB_PORT', '27017')
BLOG_DB_NAME = os.environ.get('BLOG_DB_NAME', 'py-blog')
BLOG_DB_URI = os.environ.get('BLOG_DB_URI', 'mongodb://{}:{}/{}'.format(BLOG_DB_HOST, BLOG_DB_PORT, BLOG_DB_NAME))

# aws credentials for s3 bucket storage
BLOG_FAKE_S3_HOST = os.environ.get('BLOG_FAKE_S3_HOST', 'localhost:4569')
BLOG_AWS_ACCESS_KEY_ID = os.environ.get('', '')
BLOG_AWS_SECRET_ACCESS_KEY = os.environ.get('', '')
BLOG_AWS_S3_BUCKET = os.environ.get('', 'pyblog')

# used to encrypt jwt secret key
BLOG_JWT_SECRET_KEY = os.environ.get('BLOG_JWT_SECRET_KEY', 'R3BdYF8cXJdByJWgZPZmemsN')

# used for sending emails
# TODO: add blog options, setup email verification, create email updates/alerts
BLOG_EMAIL_SMTP_HOST = os.environ.get('BLOG_EMAIL_SMTP_HOST', '0.0.0.0')
BLOG_EMAIL_SMTP_PORT = os.environ.get('BLOG_EMAIL_SMTP_PORT', 25)
BLOG_EMAIL_WEBMASTER_ADDRESS = os.environ.get('BLOG_EMAIL_WEBMASTER_ADDRESS', 'do-not-reply@mysite.com')
