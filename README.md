# py-blog

**py-blog** is a backend blog service that can easily and comfortably sit behind any frontend.

## About

This project provides a seamless REST api for your blog. py-blog has the capability to integrate with popular webservices such as Firebase hosting and aws right out of the box. This project **only** supplies you with a REST api and doesn't try to assume your use case or architecture. So why use py-blog as opposed to Wordpress, Ghost, or the various free, mature, and established platforms available? Size and flexibility.

**Project Size**

py-blog is composed of a simple RESTful api built on top of [Falcon](https://falconframework.org/), [Gunicorn](http://gunicorn.org/) WSGI and supports [resource expansion](https://stormpath.com/blog/linking-and-resource-expansion-rest-api-tips).

**Flexbility**

This project was crafted with consumability in mind. The root endpoint serves a service description that can be used as a rel/link mapping for dynamically hydrating front end interfaces. The service description helps simplify resource expansion, endpoint migration, and will allow front end developers to design their blog without having to manually construct any URLs.

*Service Description Example*

```js
[
    {
        "rel": "post-collection",
        "link": ".../posts"
    },
    {
        "rel": "authentication",
        "link": ".../user/login"
    },
    ...
]
```

*Post Collection Example*

```js
[
    {
        "href": ".../post/000000/",
        "links": [
            "rel": "like",
            "href": ".../post/000000/like"
        ],
        "title": "Foobar",
        ...
    }
]
```

**Security**

By design this blog encrypts any and all post or comment content within the given database. Blog content secret keys can be defined by the administrator, and will be hashed into a 32 bit key for AES encryption/decryption.

## Configuration

This project is highly configurable, all blog constants can be found in `blog/constants.py` and all settings can be found in `blog/settings.yml`.

**Constants** (Environmental)

* **BLOG_HOST**: Host blog will be served on for Gunicorn.
* **BLOG_PORT**: Port blog will be served on for Gunicorn.
* **BLOG_CONTENT_KEY**: Key used to encrypt/decrypt blog content.
* **BLOG_JWT_SECRET_KEY**: Key used to encrypt/decrypt session JWT.

> Note: If AWS credentials are not provided, api will alternatively store avatars and other media as base64 encoded binaries in mongodb.

* **BLOG_AWS_ACCESS_KEY_ID**: AWS access key id for s3.
* **BLOG_AWS_SECRET_ACCESS_KEY**: AWS secret access key for s3.
* **BLOG_AWS_S3_BUCKET**: AWS s3 bucket for storing avatars.

**Settings**

* **login**
  * **max_failed_login**: Minimum number of characters for usernames.
  * **failed_login_timeout**: Maximum number of characters for usernames.
* **rules**
  * **user**
    * **username_min_char**: Minimum number of characters for user full names.
    * **username_max_char**: Maximum number of characters for user full names.
    * **name_min_char**: Minimum number of characters for post titles.
    * **name_max_char**: Maximum number of characters for post titles.
  * **post**
    * **title_min_char**: Minimum number of characters for post content.
    * **title_max_char**: Minimum number of characters for post comments.
    * **content_min_char**: Maximum number of characters for post comments.
  * **comment**
    * **content_min_char**: Maximum number of consecutive failed logins.
    * **content_max_char**: Time in seconds to timeout after consecutive failed logins.

## Setting Up

The following requirements are required for staging *py-blog* for either development or production:

- mongodb 3.6
- python 3.6
- pipenv (python package manager)
- s3 bucket or fakes3 (optional)

To install the project's dependencies use:

```bash
pipenv install
```

Once the necessary configurations have been made to `blog/constants.py`, the blog can be spun up using:

```bash
pipenv run python -m blog
```

TODO: complete setup details

**Docker**

TODO: add docker setup example with sample docker-compose for setting up mongo.

## Testing

> Note: Testing will require an instance of mongodb.
> Note: CI tests s3 functionality using [fakes3](https://github.com/jubos/fake-s3) project.

The test suite is composed of operational tests exercising the blog's core, as well as mocked requests against the provided API.

To install test dependencies in your local development environment using pipenv:

```bash
pipenv install --dev
```

For running the test suite with pytest:

```bash
# without coverage
pipenv run pytest tests
# with coverage
pipenv run pytest --cov blog.core tests
```

## Deployment

TODO: cover different deployment strategies and how to use with heroku or aws ec2.

## Contributors

* **John Nolette** (john@neetgroup.net)

Basic contributing guidelines are as follows,

* Any new features must be tested properly, both from an operational level and via mocked interaction.
* Branches for bugs and features should be structured like so, `issue-x-username`.
* Include your name and email in the contributors list.

---

Copyright (c) 2018 John Nolette Licensed under the MIT License.
