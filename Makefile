.PHONY: install test lint format type-check clean

install:
	poetry install

test:
	poetry run pytest -v tests/

lint:
	poetry run flake8 .
	poetry run mypy .

format:
	poetry run black .
	poetry run isort .

type-check:
	poetry run mypy .

CI:
	make format
#	make type-check
#	make lint
	make test

run:
	poetry run python src/main.py

### Terraform
infra:
	terraform -chdir=./terraform init

infra_plan:
	terraform -chdir=./terraform plan

infra_apply:
	terraform -chdir=./terraform apply -auto-approve

infra_destroy:
	terraform -chdir=./terraform destroy -auto-approve