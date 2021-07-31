#!/usr/bin/env bash


# prints colored text
success () {
    COLOR="92m"; # green
    STARTCOLOR="\e[$COLOR";
    ENDCOLOR="\e[0m";
    printf "$STARTCOLOR%b$ENDCOLOR" "done\n";
}

echo ""
printf "Terraform Setup"
cd /workspaces/ABC-ACI/aci-terraform/
success

echo "Waiting to update Linux..."
sudo apt-get update -y
success

echo " Installing Software Properties Common"
sudo apt-get install software-properties-common -y
success

echo "Hashicorp Release"
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
success

echo "Add Repository"
sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
success

echo "Waiting to update Linux..."
sudo apt-get update -y
success

echo "Installing Terraform"
sudo apt install terraform -y
success
