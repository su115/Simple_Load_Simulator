resource "aws_dynamodb_table" "lock"{
	name="lock"
	billing_mode="PAY_PER_REQUEST"
	hash_key="LockID"
	attribute{
	name="LockID"
	type="S"
	}
}
