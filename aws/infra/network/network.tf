# VPC
resource "aws_vpc" "custom_vpc"{
	cidr_block = "10.0.0.0/16"
	tags={
		Name="Custom VPC Simple Load Simulator"
	}
}

# PUBLIC SUBNET 1
resource "aws_subnet" "public1"{
	vpc_id=aws_vpc.custom_vpc.id
	cidr_block="10.0.10.0/24"
	map_public_ip_on_launch=true
	tags = {
		Name="Custom Public Sub 1"
	}
}
# PRIVATE SUBNET 1
resource "aws_subnet" "private1"{
	vpc_id=aws_vpc.custom_vpc.id
	cidr_block="10.0.20.0/24"
	tags = {
		Name="Custom Private Sub 1"
	}
}


# INTERNET GATEWAY
resource "aws_internet_gateway" "gt"{
	vpc_id=aws_vpc.custom_vpc.id
	tags={
		Name="Internet Gateway"
	}
}

# ROUTE TABLE (control output traffic??)
resource "aws_route_table" "art"{
	vpc_id=aws_vpc.custom_vpc.id
	route{
		cidr_block="0.0.0.0/0"
		gateway_id=aws_internet_gateway.gt.id
	}
}

# ROUTE TABLE ASSOCIATION to public1 (connect RT to SUB)
resource "aws_route_table_association" "rta1"{
	subnet_id=aws_subnet.public1.id
	route_table_id=aws_route_table.art.id
}

## ROUTE TABLE ASSOCIATION to private1 (connect RT to SUB)
#resource "aws_route_table_association" "rta2"{
#	subnet_id=aws_subnet.private1.id
#	route_table_id=aws_route_table.art.id
#
#
#}no resaults

# EIP
# elastic ip
resource "aws_eip" "elastic_ip" {
  vpc      = true
}
# NAT GATEWAY
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.elastic_ip.id
  subnet_id         = aws_subnet.public1.id
}

# route table with target as NAT gateway
resource "aws_route_table" "NAT_route_table" {
  depends_on = [
    aws_vpc.custom_vpc,
    aws_nat_gateway.nat_gateway,
  ]
  vpc_id = aws_vpc.custom_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name = "NAT-route-table"
  }
}

# associate route table to private subnet
resource "aws_route_table_association" "associate_routetable_to_private_subnet" {
  depends_on = [
    aws_subnet.private1,
    aws_route_table.NAT_route_table,
  ]
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.NAT_route_table.id
}
