terraform{
    backend "s3"{
    bucket="terraform-bucket-1712"
    key="aws/infra/cluster/slave/terraform.tfstate"
    region="eu-west-1"
    dynamodb_table="lock"
    encrypt=true
    }
}

