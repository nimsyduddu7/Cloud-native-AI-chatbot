# Quick Start Guide

## ✅ Project Setup Complete!

Your Cloud-Native AI Chatbot is ready to use. Here's what's been set up:

### 🎯 Current Status
- ✅ FastAPI application running
- ✅ OpenAI API key configured
- ✅ All dependencies installed
- ✅ Server running on http://localhost:8000

### 🚀 How to Use

#### 1. Access the API Documentation
Open your browser and go to:
```
http://localhost:8000/docs
```

This will show you the interactive Swagger UI where you can test all endpoints.

#### 2. Test the Chat Endpoint

**Using the Web UI:**
1. Go to http://localhost:8000/docs
2. Click on the `/chat` endpoint
3. Click "Try it out"
4. Enter your message:
   ```json
   {
     "message": "Hello! Tell me a fun fact.",
     "session_id": "my-session-123",
     "model": "gpt-3.5-turbo"
   }
   ```
5. Click "Execute"

**Using PowerShell:**
```powershell
$body = @{
    message = "Hello! Tell me a fun fact."
    session_id = "test-123"
    model = "gpt-3.5-turbo"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/chat -Method POST -Body $body -ContentType 'application/json'
```

**Using curl:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Tell me a fun fact.",
    "session_id": "test-123",
    "model": "gpt-3.5-turbo"
  }'
```

### 📊 Available Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat` - Chat with AI
- `GET /sessions/{session_id}/history` - Get conversation history
- `DELETE /sessions/{session_id}` - Clear conversation history
- `GET /metrics` - Prometheus metrics

### 🔧 Server Management

**Start the server:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Stop the server:**
Press `Ctrl+C` in the terminal where it's running

**Check if server is running:**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

### 📝 Notes

- **Redis**: Currently not connected (optional for conversation memory)
- **Rate Limiting**: Active (60 requests/minute, 1000/hour)
- **Monitoring**: Prometheus metrics available at `/metrics`

### 🐳 Using Docker (Optional)

If you have Docker installed:
```bash
docker-compose up -d
```

This will start:
- Chatbot API (port 8000)
- Redis (port 6379)
- Prometheus (port 9090)
- Grafana (port 3001)

### 🎉 Next Steps

1. Test the API at http://localhost:8000/docs
2. Integrate it into your application
3. Deploy to AWS/Azure using the Terraform configurations
4. Set up Redis for conversation memory persistence

Enjoy your production-grade AI chatbot! 🚀
