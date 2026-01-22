variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_auth_token" {
  description = "Redis authentication token"
  type        = string
  sensitive   = true
}

variable "task_cpu" {
  description = "CPU units for ECS task (1024 = 1 vCPU)"
  type        = number
  default     = 512
}

variable "task_memory" {
  description = "Memory for ECS task in MB"
  type        = number
  default     = 1024
}

variable "service_desired_count" {
  description = "Desired number of ECS service instances"
  type        = number
  default     = 2
}

variable "certificate_arn" {
  description = "ARN of SSL certificate for load balancer"
  type        = string
}
