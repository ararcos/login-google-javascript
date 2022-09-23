POETRY=poetry
PYLINT=$(POETRY) run pylint
PACKAGE=desk_reservation
ECR_URI=$$(cd infrastructure/; terraform output base_ecr_ui | tr -d '"')
BASE_ECR_TAG=latest
LOGIN=1
AWS_REGION="us-east-1"


install:
	$(POETRY) install
	$(POETRY_EXPORT)

test:
		# @echo "=========================================Test with pytest========================================="
		# @if [ "$(specific_test)" ]; then \
		# python -m pytest -vv -s -k $(specific_test);\
		# else \
		# python -m pytest -v;\
		# fi
		# @echo "Completed test!"
lint:
	# $(PYLINT) ${PACKAGE}

hooks:
		cd .git/hooks && ln ../../.github/hooks/commit_msg.py ./commit-msg
		cd .git/hooks && ln ../../.github/hooks/pre_push.py ./pre-push
		cd .git/hooks && ln ../../.github/hooks/post_checkout.py ./post-checkout
		cd .git/hooks && ln ../../.github/hooks/pre_commit.py ./pre-commit
	

login_ecr:
	if [ "$(LOGIN)" = "1" ]; then \
		echo "LOGGING INTO THE ECR" ; \
		aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin $(ECR_URI) ; \
	else \
		echo "LOGIN SKIPPED" ; \
	fi
build_base: OSX=$(if $(filter $(shell uname -s),Darwin),1,0)
build_base: TIMESTAMP=$$(date $(if $(filter $(OSX),0),--utc,) +%Y-%m%d-%H%M-%S)
build_base: GIT_HASH=$$(git rev-parse --short HEAD)
build_base: PUSH=1
build_base: LATEST=0
build_base: Dockerfile.base
		PUSH=$(PUSH) ECR_URI=$(ECR_URI) OSX=$(OSX) \
		TIMESTAMP=$(TIMESTAMP) GIT_HASH=$(GIT_HASH) LATEST=$(LATEST) \
		DOCKER_FILE=$< ./docker_build_and_push.sh ; \
		# docker build -t $(ECR_URI):$(BASE_ECR_TAG) -f $< .
	
push_base: build_base

build_and_deploy_lambdas: OSX=$(if $(filter $(shell uname -s),Darwin),1,0)
build_and_deploy_lambdas: TIMESTAMP=$$(date $(if $(filter $(OSX),0),--utc,) +%Y-%m%d-%H%M-%S)
build_and_deploy_lambdas: GIT_HASH=$$(git rev-parse --short HEAD)
build_and_deploy_lambdas: PUSH=1
build_and_deploy_lambdas: LATEST=0
build_and_deploy_lambdas: docker_template.json

		for index in $$(jq '.[].INDEX' $<) ; do \
				echo $$index ; \
				DOCKER_BASE=$(ECR_URI) \
				LAMBDA_FILE="$$(jq -r '.['$$index'].LAMBDA_FILE' $< )"  \
				LAMBDA_HANDLER="$$(jq -r '.['$$index'].LAMBDA_HANDLER' $< )"  \
				envsubst < Dockerfile.tmpl | tee Dockerfile.tmp; \
				PUSH=$(PUSH) ECR_URI="$$(jq -r '.['$$index'].ECR_URI' $<)" OSX=$(OSX) \
				TIMESTAMP=$(TIMESTAMP) GIT_HASH=$(GIT_HASH) LATEST=$(LATEST) \
				DOCKER_FILE=Dockerfile.tmp ./docker_build_and_push.sh ; \
			done