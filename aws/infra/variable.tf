# Bucket
variable "bucket" { default = "terraform-bucket-1712" }
variable "ubuntu_ami" {default = "ami-00c90dbdc12232b58" } # Ubuntu 22 only for eu-west-1


# Machine
variable "machine" { # List
  type = map(any)    # of
  default = {        # Virtual Machines
    "slave"   = "t2.medium"	# vCPUs:1, RAM:1GB
    "master"  = "t2.medium"	# vCPUs:2, RAM:4GB 
    "bastion" = "t2.micro"	# vCPUs:1, RAM:1
  }
}

# SSH key!!! 
variable "public_key_path" { default = "/home/clone10/.ssh/id_rsa.pub"} # change!!!
variable "key_name" { default = "Summersong" }
