import os


# TODO: remove non environmental constants, add to settings.cfg and use configloader

# constants for r2dto serializer validators

EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

BLOG_USER_USERNAME_PATTERN = r'([a-zA-Z0-9]{,})$'
BLOG_USER_USERNAME_MIN_CHAR = 3
BLOG_USER_USERNAME_MAX_CHAR = 20

BLOG_USER_FNAME_MIN_CHAR = 0
BLOG_USER_FNAME_MAX_CHAR = 40

BLOG_POST_TITLE_MIN_CHAR = 3
BLOG_POST_TITLE_MAX_CHAR = 124

BLOG_POST_CONTENT_MIN_CHAR = 124

BLOG_POST_COMMENT_MIN_CHAR = 10
BLOG_POST_COMMENT_MAX_CHAR = 124

# all blog content will be cnrypted before entering the database
# likewise all blog content must be decoded

BLOG_CONTENT_KEY = os.environ.get('BLOG_CONTENT_KEY', 'mWmYSBcSzfhGuLCRvqc3A9xK')

# blog api specifications

BLOG_HOST = os.environ.get('BLOG_HOST', '0.0.0.0')
BLOG_PORT = os.environ.get('BLOG_PORT', 8080)

# aws credentials for s3 bucket storage

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

# configurations for login behavior

BLOG_MAX_FAILED_LOGIN = 5
BLOG_FAILED_LOGIN_TIMEOUT = 300
