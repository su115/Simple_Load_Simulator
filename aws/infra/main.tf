resource "aws_instance" "app_server" {
  ami           = "ami-00c90dbdc12232b58"
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}

