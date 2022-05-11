resource "aws_s3_bucket" "state"{
	bucket=var.bucket
	force_destroy=true
	versioning{
		enabled=false
		}
	server_side_encryption_configuration{
		rule{
			apply_server_side_encryption_by_default{
				sse_algorithm="AES256"
				}
			}
		}
}
