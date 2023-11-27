locals {
  vpc_id           = "vpc-04c38fe19797b30d8"
  subnet_id        = "subnet-0a4696954ed23e77c"
  ssh_user         = "ubuntu"
  key_name         = "sinda"
  private_key_path = "~/.ssh/sinda.pem"
}

provider "aws" {
  region = "us-east-1"
  profile = "sinda"
}

resource "aws_security_group" "nginx" {
  name   = "nginx_access"
  vpc_id = local.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 8050
    to_port     = 8050
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "nginx" {
  ami                         = "ami-053b0d53c279acc90"
  subnet_id                   = local.subnet_id
  instance_type               = "t2.medium"
  associate_public_ip_address = true
  security_groups             = [aws_security_group.nginx.id]
  key_name                    = local.key_name

  provisioner "remote-exec" {
    inline = ["echo 'Wait until SSH is ready'"]

    connection {
      type        = "ssh"
      user        = local.ssh_user
      private_key = file(local.private_key_path)
      host        = aws_instance.nginx.public_ip
    }
  }
  provisioner "local-exec" {
    command = "ansible-playbook  -i ${aws_instance.nginx.public_ip}, --private-key ${local.private_key_path} nginx.yaml"
  }
}

output "nginx_ip" {
  value = aws_instance.nginx.public_ip
}
