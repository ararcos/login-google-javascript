POETRY=poetry
PYLINT=$(POETRY) run pylint --extension-pkg-whitelist='pydantic'
PACKAGE=desk_reservation
ENVIRONMENT=prod
ENVIRONMENT_SUFFIX=
ECR_URI=$$(cd infrastructure/$(ENVIRONMENT); terraform output base_ecr_ui | tr -d '"')
COMMIT_ID=$$(git rev-parse HEAD)
BASE_ECR_TAG=latest
LOGIN=1
AWS_REGION="us-east-1"


install:
	$(POETRY) install
	$(POETRY_EXPORT)

test:
		@echo "=========================================Test with pytest========================================="
		@if [ "$(specific_test)" ]; then \
		python -m pytest -vv -s -k $(specific_test);\
		else \
		python -m pytest -v;\
		fi
		@echo "Completed test!"
lint:
		$(PYLINT) ${PACKAGE}

hooks:
		cd .git/hooks && ln ../../.github/hooks/commit_msg.py ./commit-msg
		cd .git/hooks && ln ../../.github/hooks/pre_push.py ./pre-push
		cd .git/hooks && ln ../../.github/hooks/post_checkout.py ./post-checkout
		cd .git/hooks && ln ../../.github/hooks/pre_commit.py ./pre-commit
	
base.tar: desk_reservation .env
		tar -cvf $@ $^

login_ecr:
	if [ "$(LOGIN)" = "1" ]; then \
		echo "LOGGING INTO THE ECR" ; \
		aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin $(ECR_URI) ; \
	else \
		echo "LOGIN SKIPPED" ; \
	fi

build_base: Dockerfile.base base.tar
		docker build -t $(ECR_URI):$(BASE_ECR_TAG) -f $< .
	
push_base: build_base
		docker push $(ECR_URI):$(BASE_ECR_TAG)

build_and_deploy_cors: CORS_TAG=latest
build_and_deploy_cors:
		docker pull $(ECR_REGISTRY)/$(CORS_NAME):$(CORS_TAG) || (\
			docker build -t $(ECR_REGISTRY)/$(CORS_NAME):$(CORS_TAG) -f Dockerfile.cors . && \
			docker push $(ECR_REGISTRY)/$(CORS_NAME):$(CORS_TAG) \
		)

build_and_deploy_lambdas: PUSH=1
build_and_deploy_lambdas: LOGIN=1
build_and_deploy_lambdas: docker_template.json login_ecr
	for index in $$(jq '.[].INDEX' $<) ; do \
		DOCKER_BASE=$(ECR_URI) \
		BASE_TAG=$(BASE_ECR_TAG) \
		LAMBDA_FILE="$$(jq -r '.['$$index'].LAMBDA_FILE' $< )"  \
		LAMBDA_HANDLER="$$(jq -r '.['$$index'].LAMBDA_HANDLER' $< )"  \
		envsubst < Dockerfile.tmpl | tee Dockerfile.tmp; \
		docker build -t $(ECR_REGISTRY)/"$$(jq -r '.['$$index'].ECR_NAME' $<)$(ENVIRONMENT_SUFFIX)":$(BASE_ECR_TAG) -f Dockerfile.tmp . ; \
		if [ "$(PUSH)" = "1" ] ; then \
			docker push $(ECR_REGISTRY)/"$$(jq -r '.['$$index'].ECR_NAME' $<)$(ENVIRONMENT_SUFFIX)":$(BASE_ECR_TAG) ; \
		fi ; \
	done
