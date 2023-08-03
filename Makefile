# Variables
DOCKER_HUB_USERNAME := hiroki11hanada
REPOSITORY_NAME := rca-batch
TAG ?= latest
ENGINE ?= docker
IMAGE_NAME := $(DOCKER_HUB_USERNAME)/$(REPOSITORY_NAME):$(TAG)
NAMESPACE ?= default

# Conditionally set the BUILD_COMMAND and PUSH_COMMAND
ifeq ($(ENGINE),docker)
	BUILD_COMMAND=docker buildx build --platform linux/amd64 -t $(IMAGE_NAME) . --load
	BUILD_COMMAND_ARM64=docker buildx build --platform linux/arm64 -t $(IMAGE_NAME) . --load
	BUILD_COMMAND_ALL=docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME) . --push
	PUSH_COMMAND=docker push $(IMAGE_NAME)
else ifeq ($(ENGINE),podman)
	BUILD_COMMAND=podman build --platform linux/amd64 -t $(IMAGE_NAME) .
	BUILD_COMMAND_ARM64=podman build --platform linux/arm64 -t $(IMAGE_NAME) .
	BUILD_COMMAND_ALL=podman build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME) .
	PUSH_COMMAND=podman push $(IMAGE_NAME)
else
$(error ENGINE must be either 'docker' or 'podman')
endif

.PHONY: dev release push all deploy

dev:
	$(BUILD_COMMAND_ARM64)
	$(PUSH_COMMAND)

release:
	$(BUILD_COMMAND)
	$(PUSH_COMMAND)

push:
	$(PUSH_COMMAND)

all:
	$(BUILD_COMMAND_ALL)
	$(PUSH_COMMAND)

deploy:
	bash k8s/prepare_secret.sh -n $(NAMESPACE)
	kubectl apply -k k8s/overlays/development -n $(NAMESPACE)
