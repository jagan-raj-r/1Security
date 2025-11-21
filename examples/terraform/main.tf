# Example Terraform configuration with intentional security issues
# This is for testing Checkov integration

# Provider configuration
provider "aws" {
  region = "us-east-1"
}

# Example S3 bucket with security issues
resource "aws_s3_bucket" "example" {
  bucket = "my-insecure-bucket"
  
  # ISSUE: No encryption enabled
  # ISSUE: No versioning enabled
}

# Example S3 bucket ACL - public access (BAD!)
resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.example.id
  acl    = "public-read"  # ISSUE: Public access enabled
}

# Example security group with overly permissive rules
resource "aws_security_group" "example" {
  name        = "example-sg"
  description = "Example security group"
  
  # ISSUE: Allows SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH from anywhere"
  }
  
  # ISSUE: Allows all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Example RDS instance with security issues
resource "aws_db_instance" "example" {
  identifier           = "example-db"
  engine              = "mysql"
  engine_version      = "5.7"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  username            = "admin"
  password            = "password123"  # ISSUE: Hardcoded password
  skip_final_snapshot = true
  
  # ISSUE: No encryption at rest
  # ISSUE: Publicly accessible
  publicly_accessible = true
  
  # ISSUE: No backup retention
  backup_retention_period = 0
}

# Example IAM policy with overly permissive permissions
resource "aws_iam_policy" "example" {
  name        = "example-policy"
  description = "Example IAM policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "*"  # ISSUE: Allows all actions
        Resource = "*"  # ISSUE: On all resources
      }
    ]
  })
}

