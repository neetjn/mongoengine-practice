from alley import Migrations
from blog.blog import api
from blog.constants import BLOG_HOST, BLOG_PORT, BLOG_WORKERS, BLOG_RUN_MIGRATIONS
from blog.db import db
import gunicorn.app.base
import os


MIGRATION_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BlogStandalone(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(BlogStandalone, self).__init__()

    def load_config(self):
        config = dict(
            [(key, value) for key, value in self.options.items() if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    if BLOG_RUN_MIGRATIONS:
        # run database migrations before starting application
        Migrations(MIGRATION_PATH, db).up()
    options = {
        'bind': f'{BLOG_HOST}:{BLOG_PORT}',
        'workers': BLOG_WORKERS,
    }
    BlogStandalone(api, options).run()
