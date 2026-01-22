# Cloud-Native AI Chatbot (Production-Grade)

A production-ready, cloud-native AI chatbot built with FastAPI, OpenAI, Redis, and comprehensive monitoring. Designed for deployment on AWS or Azure with Docker, Terraform, and Prometheus/Grafana.

##  Features

- **LLM-Powered Chatbot**: OpenAI integration with support for multiple models
- **Context Memory**: Redis-based conversation history management
- **Rate Limiting**: Distributed rate limiting with Redis fallback
- **Comprehensive Logging**: Request/response logging with structured logs
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Cloud Deployment**: Terraform configurations for AWS and Azure
- **Dockerized**: Complete Docker Compose setup for local development
- **Production-Ready**: Health checks, error handling, and scalability features

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Redis (or use Docker Compose)
- OpenAI API key
- Terraform (for cloud deployment)
- AWS CLI / Azure CLI (for cloud deployment)

##  Quick Start

### Local Development with Docker Compose

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-agent-pipeline
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Grafana: http://localhost:3001 (admin/admin)
   - Prometheus: http://localhost:9090

### Local Development (Without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis** (if not using Docker)
   ```bash
   redis-server
   ```

3. **Set environment variables**
   ```bash
   export OPENAI_API_KEY=your-api-key
   export REDIS_HOST=localhost
   export REDIS_PORT=6379
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📡 API Endpoints

### Chat
- `POST /chat` - Send a message and get AI response
  ```json
  {
    "message": "Hello, how are you?",
    "session_id": "user-123",
    "model": "gpt-3.5-turbo"
  }
  ```

### Session Management
- `GET /sessions/{session_id}/history` - Get conversation history
- `DELETE /sessions/{session_id}` - Clear conversation history

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics endpoint

## 🐳 Docker

### Build Image
```bash
docker build -t ai-chatbot:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  ai-chatbot:latest
```

## ☁️ Cloud Deployment

### AWS Deployment

1. **Configure Terraform**
   ```bash
   cd terraform/aws
   terraform init
   ```

2. **Set variables**
   ```bash
   export TF_VAR_redis_auth_token=your-redis-token
   export TF_VAR_certificate_arn=arn:aws:acm:...
   ```

3. **Deploy**
   ```bash
   terraform plan
   terraform apply
   ```

4. **Push Docker image to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ecr-url>
   docker tag ai-chatbot:latest <ecr-url>:latest
   docker push <ecr-url>:latest
   ```

### Azure Deployment

1. **Configure Terraform**
   ```bash
   cd terraform/azure
   terraform init
   ```

2. **Set variables**
   ```bash
   export TF_VAR_openai_api_key=your-openai-key
   ```

3. **Deploy**
   ```bash
   terraform plan
   terraform apply
   ```

4. **Push Docker image to ACR**
   ```bash
   az acr login --name <acr-name>
   docker tag ai-chatbot:latest <acr-name>.azurecr.io/chatbot:latest
   docker push <acr-name>.azurecr.io/chatbot:latest
   ```

## 📊 Monitoring

### Prometheus Metrics

The application exposes metrics at `/metrics`:
- `chatbot_requests_total` - Total requests
- `chatbot_responses_total` - Total responses
- `chatbot_errors_total` - Total errors
- `chatbot_request_duration_seconds` - Request duration
- `chatbot_active_requests` - Active requests
- `chatbot_tokens_used` - Token usage
- `chatbot_active_sessions` - Active sessions

### Grafana Dashboard

Access Grafana at http://localhost:3001 and import the dashboard from `monitoring/grafana/dashboards/chatbot-dashboard.json`.

## ⚙️ Configuration

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_PASSWORD` | Redis password | Empty |
| `RATE_LIMIT_PER_MINUTE` | Rate limit per minute | `60` |
| `RATE_LIMIT_PER_HOUR` | Rate limit per hour | `1000` |
| `CORS_ORIGINS` | CORS allowed origins | `http://localhost:3000` |
| `DEBUG` | Debug mode | `False` |

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FastAPI   │────▶│   OpenAI    │     │   Redis     │
│  (Chatbot)  │     │     API     │     │  (Memory)   │
└──────┬──────┘     └─────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│ Prometheus  │────▶│   Grafana   │
│  (Metrics)  │     │ (Dashboard) │
└─────────────┘     └─────────────┘
```

## 🔒 Security

- Rate limiting to prevent abuse
- Redis authentication support
- Secrets management via AWS Secrets Manager / Azure Key Vault
- HTTPS/TLS encryption
- Input validation and sanitization

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues and questions, please open an issue on GitHub.
