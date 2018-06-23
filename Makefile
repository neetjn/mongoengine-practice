PRODUCT_OWNER := neetjn
PRODUCT_NAME := py-blog
PRODUCT_VERSION := 0.0.0

PRODUCT_IMAGE := ${PRODUCT_OWNER}/${PRODUCT_NAME}:${PRODUCT_VERSION}
PRODUCT_TEST_IMAGE := ${PRODUCT_OWNER}/${PRODUCT_NAME}:test
MONGODB_IMAGE := mongo:3.6

build:
  docker build . -t ${PRODUCT_IMAGE}
  docker build . -f tests/Dockerfile -t ${PRODUCT_TEST_IMAGE}

test:
  @echo Spinning up mongodb instance


test-clean:
  docker rm -f test-${}

publish:

