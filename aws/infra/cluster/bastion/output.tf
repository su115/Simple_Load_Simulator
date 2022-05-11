output "all_ip"{
value = flatten( aws_instance.server.*.public_ip )

}
