variable "aws-region" {
  type    = string
  default = "us-east-1"
}

variable "aws_profile" {
  type    = string
  default = "rahul-dev"
}
variable "source_ami" {
  type    = string
  default = "ami-0440d3b780d96b29d"
}

variable "ssh_username" {
  type    = string
  default = "ec2-user"
}

variable "subnet_id" {
  type    = string
  default = "subnet-0016ed8ae147e5fe5"
}
variable "aws-access-key-id" {
  type    = string
  default = env("aws-access-key-id")
}

variable "aws-secret-access-key" {
  type    = string
  default = env("aws-secret-access-key")
}
variable "ami_user" {
  type    = list(string)
  default = ["058264062390"]
}

source "amazon-ebs" "my-ami" {
  ami_name        = "fastapi_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = " AMI for Fast API"
  instance_type   = "t2.micro"
  region          = "${var.aws-region}"
  profile         = "${var.aws_profile}"
  ssh_username    = "${var.ssh_username}"
  subnet_id       = "${var.subnet_id}"
  source_ami      = "${var.source_ami}"
  access_key      = "${var.aws-access-key-id}"
  secret_key      = "${var.aws-secret-access-key}"
  ami_users       = "${var.ami_user}"
  ami_regions = [
    var.aws-region
  ]
  aws_polling {
    delay_seconds = 120
    max_attempts  = 50
  }

  ami_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/xvda"
    volume_size           = 8
    volume_type           = "gp2"
  }
}

build {
  name = "build-packer"
  sources = [
    "source.amazon-ebs.my-ami"
  ]

  provisioner "file" {
    source      = "fast-api-webapp-0.0.1.zip"
    destination = "fast-api-webapp-0.0.1.zip"
  }

  #  provisioner "file" {
  #    source      = "cloudwatch-config.json"
  #    destination = "/tmp/cloudwatch-config.json"
  #  }
  provisioner "shell" {
    script = "script.sh"
  }

  provisioner "file" {
    source      = "webservice.service"
    destination = "/tmp/"
  }

  #   post-processor "manifest" {
  #    output = "manifest.json"
  #    strip_path = true
  #  }


  provisioner "shell" {
    inline = [
      "sudo chmod 770 /home/ec2-user/fast-api-webapp-0.0.1.zip",
      "sudo unzip -o fast-api-webapp-0.0.1.zip",
      "cd fast-api-webapp-0.0.1",
      "sudo python3.11 -m venv venv",
      "source venv/bin/activate",
      "sudo chown -R ec2-user:ec2-user /home/ec2-user/fast-api-webapp-0.0.1/venv",
      "cd app",
      "pip3.11 install -r requirements.txt",
      "cd /home/ec2-user/fast-api-webapp-0.0.1/venv/bin",
      "sudo cp /tmp/webservice.service /etc/systemd/system",
      "sudo chmod 770 /etc/systemd/system/webservice.service",
      "sudo systemctl start webservice.service",
      "sudo systemctl enable webservice.service",
      "sudo systemctl restart webservice.service",
      "sudo systemctl status webservice.service",
      "echo '****** Copied webservice! *******'"
    ]
  }

}