# INSTANCE
resource "aws_instance" "server"{
  ami           = var.ubuntu_ami
  instance_type = var.machine["bastion"]
  vpc_security_group_ids = [local.public_sg_id, local.private_sg_id]
  count = 1
  associate_public_ip_address = true
  key_name = local.ssh_key_id
  subnet_id=local.public1_id
  tags = {
    Name = "Ubuntu-bastion"
  }
}
