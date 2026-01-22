.PHONY: help build up down logs test clean deploy

help: ## Show this help message
	@echo "Cloud-Native AI Chatbot - Makefile Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs from all services
	docker-compose logs -f

logs-app: ## View logs from chatbot service
	docker-compose logs -f chatbot

restart: ## Restart all services
	docker-compose restart

clean: ## Remove all containers, volumes, and images
	docker-compose down -v --rmi all

test: ## Run API tests
	bash scripts/test_api.sh

deploy: ## Deploy using deployment script
	bash scripts/deploy.sh

health: ## Check service health
	curl -f http://localhost:8000/health | jq '.'

install: ## Install Python dependencies locally
	pip install -r requirements.txt

run-local: ## Run application locally (requires Redis)
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

terraform-aws-init: ## Initialize Terraform for AWS
	cd terraform/aws && terraform init

terraform-aws-plan: ## Plan Terraform deployment for AWS
	cd terraform/aws && terraform plan

terraform-aws-apply: ## Apply Terraform deployment for AWS
	cd terraform/aws && terraform apply

terraform-azure-init: ## Initialize Terraform for Azure
	cd terraform/azure && terraform init

terraform-azure-plan: ## Plan Terraform deployment for Azure
	cd terraform/azure && terraform plan

terraform-azure-apply: ## Apply Terraform deployment for Azure
	cd terraform/azure && terraform apply
