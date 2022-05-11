data "terraform_remote_state" "network"{
	backend = "s3"
	config={
		bucket=var.bucket
		key="aws/infra/network/terraform.tfstate"
		region="eu-west-1"
	}
}

locals {
	vpc_id=data.terraform_remote_state.network.outputs.vpc_id
	public1_id=data.terraform_remote_state.network.outputs.public1_id
	private1_id=data.terraform_remote_state.network.outputs.private1_id
    public_sg_id=data.terraform_remote_state.network.outputs.public_sg_id
    private_sg_id=data.terraform_remote_state.network.outputs.private_sg_id
    ssh_key_id=data.terraform_remote_state.network.outputs.ssh_key_id    
}
