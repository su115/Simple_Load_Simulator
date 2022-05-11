output "master-private-ip" {
  value = flatten( aws_instance.master.*.private_ip )
}
