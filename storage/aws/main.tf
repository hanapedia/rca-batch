variable "aws_region" {
  description = "AWS region."
  type        = string
}

variable "bucket_name" {
  description = "Name of the s3 bucket to create"
  type        = string
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = "rca-batch"
    Description = "Bucket to store results of rca-batch job."
  }
}

output "bucket_url" {
  description = "The URL of the bucket"
  value       = "s3://${aws_s3_bucket.bucket.bucket_domain_name}"
}
