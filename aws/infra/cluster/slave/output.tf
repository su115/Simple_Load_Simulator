output "slave-private-ips" {
  value = flatten( aws_instance.slave.*.private_ip )
}
