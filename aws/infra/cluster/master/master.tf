# INSTANCE
resource "aws_instance" "master"{
  ami           = var.ubuntu_ami
  instance_type = var.machine["master"]
  vpc_security_group_ids = [local.private_sg_id]
  count = 1
  key_name = local.ssh_key_id
  subnet_id=local.private1_id
  root_block_device {
      tags                  = {}
      volume_size           = 20
  }
  tags = {
    Name = "Ubuntu-master"
  }
}

