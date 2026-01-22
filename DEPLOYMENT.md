# Deployment Guide

## Quick Start

### Local Development

1. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Start services**
   ```bash
   make up
   # or
   docker-compose up -d
   ```

3. **Access services**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Grafana: http://localhost:3001
   - Prometheus: http://localhost:9090

## AWS Deployment

### Prerequisites
- AWS CLI configured
- Terraform installed
- Docker installed
- ECR repository access

### Steps

1. **Initialize Terraform**
   ```bash
   cd terraform/aws
   terraform init
   ```

2. **Configure variables**
   Create `terraform.tfvars`:
   ```hcl
   aws_region = "us-east-1"
   redis_auth_token = "your-secure-token"
   certificate_arn = "arn:aws:acm:..."
   task_cpu = 512
   task_memory = 1024
   service_desired_count = 2
   ```

3. **Plan deployment**
   ```bash
   terraform plan
   ```

4. **Deploy infrastructure**
   ```bash
   terraform apply
   ```

5. **Build and push Docker image**
   ```bash
   # Get ECR login
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin <ecr-url>
   
   # Build image
   docker build -t chatbot:latest .
   
   # Tag and push
   docker tag chatbot:latest <ecr-url>:latest
   docker push <ecr-url>:latest
   ```

6. **Update ECS service**
   ```bash
   aws ecs update-service \
     --cluster chatbot-cluster \
     --service chatbot-service \
     --force-new-deployment
   ```

## Azure Deployment

### Prerequisites
- Azure CLI installed and logged in
- Terraform installed
- Docker installed

### Steps

1. **Initialize Terraform**
   ```bash
   cd terraform/azure
   terraform init
   ```

2. **Configure variables**
   Create `terraform.tfvars`:
   ```hcl
   resource_group_name = "chatbot-rg"
   location = "eastus"
   openai_api_key = "your-openai-key"
   acr_name = "chatbotacr"
   app_service_name = "chatbot-app"
   ```

3. **Plan deployment**
   ```bash
   terraform plan
   ```

4. **Deploy infrastructure**
   ```bash
   terraform apply
   ```

5. **Build and push Docker image**
   ```bash
   # Login to ACR
   az acr login --name <acr-name>
   
   # Build and push
   az acr build --registry <acr-name> --image chatbot:latest .
   ```

6. **Restart App Service**
   ```bash
   az webapp restart --name <app-service-name> --resource-group <resource-group>
   ```

## Environment Variables

Required environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `REDIS_HOST` - Redis hostname
- `REDIS_PORT` - Redis port (default: 6379)
- `REDIS_PASSWORD` - Redis password (optional)
- `RATE_LIMIT_PER_MINUTE` - Rate limit per minute (default: 60)
- `RATE_LIMIT_PER_HOUR` - Rate limit per hour (default: 1000)

## Monitoring

### Prometheus
- Access at http://localhost:9090
- Metrics endpoint: http://localhost:8000/metrics

### Grafana
- Access at http://localhost:3001
- Default credentials: admin/admin
- Dashboard automatically provisioned

## Troubleshooting

### Service not starting
```bash
docker-compose logs chatbot
```

### Redis connection issues
```bash
docker-compose logs redis
redis-cli -h localhost -p 6379 ping
```

### Check health
```bash
curl http://localhost:8000/health
```

## Scaling

### AWS ECS
Update `service_desired_count` in Terraform or use:
```bash
aws ecs update-service \
  --cluster chatbot-cluster \
  --service chatbot-service \
  --desired-count 4
```

### Azure App Service
Scale via Azure Portal or CLI:
```bash
az appservice plan update \
  --name <plan-name> \
  --resource-group <resource-group> \
  --sku S2
```
