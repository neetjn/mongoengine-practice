# py-blog

[![build](https://travis-ci.org/neetjn/py-blog.svg?branch=master)](https://travis-ci.org/neetjn/py-blog)
[![codecov](https://codecov.io/gh/neetjn/py-blog/branch/master/graph/badge.svg)](https://codecov.io/gh/neetjn/py-blog)
[![docker-automated](https://img.shields.io/docker/cloud/automated/neetjn/py-blog.svg)](https://cloud.docker.com/repository/docker/neetjn/py-blog/general)
[![docker-build](https://img.shields.io/docker/cloud/build/neetjn/py-blog.svg)](https://cloud.docker.com/repository/docker/neetjn/py-blog/general)


**py-blog** is a backend blog service that can easily and comfortably sit behind any frontend.

## Why

I used this project as an opportunity to learn Falcon, a minimal RESTful framework for Python.

## About

This project provides a seamless REST api for your blog. py-blog has the capability to integrate with popular webservices such as aws right out of the box. This project **only** supplies you with a REST api and doesn't try to assume your use case or architecture. So why use py-blog as opposed to Wordpress, Ghost, or the various free, mature, and established platforms available? Size and flexibility.

**Project Size**

py-blog is composed of a simple RESTful api built on top of [Falcon](https://falconframework.org/) and [Gunicorn](http://gunicorn.org/) WSGI designed with HATEOAS ([resource expansion](https://stormpath.com/blog/linking-and-resource-expansion-rest-api-tips)).

**Flexbility**

This project was crafted with consumability in mind. The root endpoint serves a service description that can be used as a rel/link mapping for dynamically hydrating front end interfaces. The service description helps simplify resource expansion, endpoint migration, and will allow front end developers to design their blog without having to manually construct any URLs.

*Service Description Example*

```js
{
  "links": [
    {
      "rel": "post-collection",
      "href": "localhost:8000/v1/posts/",
      "acceptedMethods": [
        "GET",
        "POST"
      ]
    },
    {
      "rel": "post-search",
      "href": "localhost:8000/v1/posts/search/",
      "acceptedMethods": [
        "POST"
      ]
    },
    {
      "rel": "user-authentication",
      "href": "localhost:8000/v1/user/authenticate/",
      "acceptedMethods": [
        "POST"
      ]
    },
    {
      "rel": "user",
      "href": "localhost:8000/v1/user/",
      "acceptedMethods": [
        "GET",
        "PUT"
      ]
    },
    {
      "rel": "user-registration",
      "href": "localhost:8000/v1/user/register/",
      "acceptedMethods": [
        "POST"
      ]
    }
  ]
}
```

*Post Collection Example*

```js
{
  "posts": [
    {
      "href": "localhost:8000/v1/post/5b776070df72ea7bdeb80a19/",
      "author": "John Nolette",
      "title": "My First Post",
      "description": "This is my first post ever!",
      "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
      "tags": [
        "hello",
        "world"
      ],
      "private": false,
      "featured": false,
      "created": "2018-08-17 23:55:28.206000",
      "edited": null,
      "comments": 0,
      "likes": 0,
      "views": 0,
      "links": [
        {
          "rel": "self",
          "href": "localhost:8000/v1/post/5b776070df72ea7bdeb80a19/",
          "acceptedMethods": [
            "GET",
            "PUT",
            "DELETE"
          ]
        },
        {
          "rel": "post-comment",
          "href": "localhost:8000/v1/post/5b776070df72ea7bdeb80a19/comment",
          "acceptedMethods": [
            "POST"
          ]
        },
        {
          "rel": "post-like",
          "href": "localhost:8000/v1/post/5b776070df72ea7bdeb80a19/like",
          "acceptedMethods": [
            "PUT"
          ]
        },
        {
          "rel": "post-view",
          "href": "localhost:8000/v1/post/5b776070df72ea7bdeb80a19/view",
          "acceptedMethods": [
            "PUT"
          ]
        }
      ]
    }
  ]
}
```

**Security**

By design this blog encrypts any and all post or comment content within the given database. Blog content secret keys can be defined by the administrator, and will be hashed into a 32 bit key for AES encryption/decryption.

**Features**

The py-blog project ships with (but is not limited to) the following:

* [x] Service Description (resource expansion)
* [x] Logging
* [x] User Registration/Authentication (includes login failure handling)
* [ ] Email verification
* [x] User Roles (blogger, moderator, admin)
* [ ] User news letters
* [X] User avatars and avatar storage
* [X] AWS S3 support for media management
* [x] Live blog settings management
* [x] Creating, deleting, liking, "viewing" posts
* [x] Fetching all public posts (with pagination)
* [x] Post privacy (editing/publishing)
* [x] Featured posts
* [x] Post content encryption (database level)
* [x] Searching for posts by title, description, content, and author (with cooldown and pagination)
* [x] Creating, deleting, liking post comments
* [x] Comment content encryption (database level)
* [x] Resource caching.

## Configuration

This project is highly configurable, all blog constants can be found in `blog/constants.py` and all settings can be found in `blog/settings.yml`.

**Constants** (Environmental)

* **BLOG_TEST**: Provision platform for test environments.
* **BLOG_HOST**: Host blog will be served on for Gunicorn.
* **BLOG_PORT**: Port blog will be served on for Gunicorn.
* **BLOG_REDIS_HOST**: Blog redis host for caching.
* **BLOG_DB_HOST**: Blog mongodb database host.
* **BLOG_CONTENT_KEY**: Key used to encrypt/decrypt blog content.
* **BLOG_JWT_SECRET_KEY**: Key used to encrypt/decrypt session JWT.

> Note: If AWS credentials are not provided, api will alternatively store avatars and other media as base64 encoded binaries in mongodb.

* **BLOG_FAKE_S3_HOST**: fakes3 host for blog to use in test mode.
* **BLOG_AWS_ACCESS_KEY_ID**: AWS access key id for s3.
* **BLOG_AWS_SECRET_ACCESS_KEY**: AWS secret access key for s3.
* **BLOG_AWS_S3_BUCKET**: AWS s3 bucket for storing avatars.

**Settings**

* **login**
  * **max_failed_login**: Maximum number of consecutive failed logins.
  * **failed_login_timeout**: Time in seconds to timeout after consecutive failed logins.
  * **max_session_time**: Time in seconds a session is valid after a token is generated.
* **post**
  * **view_time_delay**: Time in seconds wait before processing another post view.
  * **search_time_delay**: Time in seconds to wait in between each post search request.
* **user**
  * **allow_avatar_capability**: Allow avatars to be uploaded and served.
  * **allow_manual_registration**: Allow manual registration for new users, enabled registration endpoint.
  * **require_email_verification**: Enforce email verification for new users.
  * **upload_avatar_s3**: Upload avatar to s3 instead of mongodb gridfs storage.
* **rules**
  * **user**
    * **avatar_size**: Maximum size in kb for uploaded user avatars.
    * **username_min_char**: Minimum number of characters for user names.
    * **username_max_char**: Maximum number of characters for user names.
    * **name_min_char**: Minimum number of characters for post titles.
    * **name_max_char**: Maximum number of characters for post titles.
  * **post**
    * **title_min_char**: Minimum number of characters for post titles.
    * **title_max_char**: Maximum number of characters for post titles.
    * **content_min_char**: Minimum number of characters for post content.
    * **content_max_char**: Maximum number of characters for post content.
    * **tag_min_char**: Minimum number of characters for a single post tag.
    * **tag_max_char**: Maximum number of characters for a single post tag.
    * **tag_max_count**: Maximum number of tags a post can have.
  * **comment**
    * **content_min_char**: Minimum number of characters for comments.
    * **content_max_char**: Maximum number of characters for comments.

## Setting Up

The following requirements are required for staging *py-blog* for either development or production:

- python 3.6
- mongodb 3.6
- redis 4
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

For provisioning refer to the [**Configuration**](https://github.com/neetjn/py-blog#configuration) section.

**Docker**

Build your docker image:

```bash
docker build . -t py-blog
```

Run your container:

```bash
docker run --name blog -p 8000:8000 py-blog
```

Alternatively use `docker-compose` for a quick start, will provide a mongodb container:

```bash
docker-compose up
```

## Testing

> Note: Testing will require an instance of mongodb.
> Note: CI tests s3 functionality using [fakes3](https://github.com/jubos/fake-s3) project.

The test suite is composed of operational tests exercising the blog's core, as well as mocked requests against the provided API using the [falcon testing tools](http://falcon.readthedocs.io/en/stable/api/testing.html).

To install test dependencies in your local development environment using pipenv:

```bash
pipenv install --dev
```

For running the test suite with pytest:

```bash
# without coverage
BLOG_TEST=TRUE pipenv run pytest tests
# with coverage
BLOG_TEST=TRUE pipenv run pytest --cov blog.core tests
```

Alternatively, you may run your tests within a docker container using:

```bash
make build test test-clean
```

## Contributors

* **John Nolette** (john@neetgroup.net)

Basic contributing guidelines are as follows,

* Any new features must be tested properly, both from an operational level and via mocked interaction.
* Branches for bugs and features should be structured like so, `issue-x-username`.
* Include your name and email in the contributors list.

---

Copyright (c) 2019 John Nolette Licensed under the MIT License.
