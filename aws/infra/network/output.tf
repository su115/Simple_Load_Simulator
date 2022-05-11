output "vpc_id"{
	value=aws_vpc.custom_vpc.id
}

output "public1_id"{
	value=aws_subnet.public1.id
}
output "private1_id"{
	value=aws_subnet.private1.id
}
output "public_sg_id"{
    value=aws_security_group.public.id
}
output "private_sg_id"{
    value=aws_security_group.private.id
}


output "ssh_key_id" {
    value=aws_key_pair.auth.id
}
