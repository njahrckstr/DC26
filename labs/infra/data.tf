#
# Data
#

data "external" "user_list" {
  program = [
    "bash",
    "-c",
    "map=$(for l in $(cat users/user-list.csv); do echo -n \"\\\"$(echo -n $l | cut -d ',' -f 1)\\\":\\\"\\\",\"; done); echo -e \"{$${map%?}}\" | tr -d '\r'"
  ]
}

data "external" "my_ip" {
  program = [
    "bash",
    "-c",
    "echo \"{\\\"ip\\\":\\\"$(curl ipinfo.io/ip)\\\"}\""
  ]
}

data "template_file" "floodlight_init" {
  count = "${var.workstation_count}"
  template = "${file("templates/init.tpl")}"

  vars {
    user = "${element(keys(data.external.user_list.result), count.index)}"
  }
}