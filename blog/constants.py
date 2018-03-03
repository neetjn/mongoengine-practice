import os


BLOG_HOST = os.environ.get('BLOG_HOST', '0.0.0.0')
BLOG_PORT = os.environ.get('BLOG_PORT', 8080)

BLOG_AWS_ACCESS_KEY_ID = os.environ.get('', '')
BLOG_AWS_SECRET_ACCESS_KEY = os.environ.get('', '')
BLOG_AWS_SESSION_TOKEN = os.environ.get('', '')
BLOG_AWS_S3_BUCKET = os.environ.get('', 'pyblog')

BLOG_JWT_SECRET_KEY = os.environ.get('BLOG_JWT_SECRET_KEY', 'R3BdYF8cXJdByJWgZPZmemsN')
