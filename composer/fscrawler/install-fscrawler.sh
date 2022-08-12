#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "Please run this script as sudo"
	exit 1
fi

default_username=fscrawler
default_password=fscrawler

# ----------------------------------
username=$default_username
password=$default_password
job_name=""

help() {
	printf "Usage: $0 [-u USERNAME] [ -p PASSWORD ] JOB_NAME\n\n"

	printf "OPTIONS:\n"

	printf "\t-u USERNAME\tUsername for user created for fscrawler \n"
	printf "\t\tDefault: $default_username\n"

	printf "\t-p PASSWORD\tPassword for user created for fscrawler service\n"
	printf "\t\tDefault: $default_password\n"

	printf "\tJOB_NAME\tName of the fscrawler job (named after ES index)\n\n"
}

if [ $# = 0 ]; then
	help
	exit 1
fi

check_for_empty() {
	if [ "$1" = "" ]; then
		help
		return 1
	fi

	return 0
}

for ((i=1; i <= $#; i++)); do
	arg=$((i+1))
	case "${!i}" in
		-u )
			check_for_empty "${!arg}" || (help && exit 1)
			username=${!arg}
			i=$((i+1))
			;;
		-p )
			check_for_empty "${!arg}" || (help && exit 1)
			password=${!arg}
			i=$((i+1))
			;;
		-h | --help )
			help
			exit 0
			;;
		*)
			job_name=${!i}
			;;
	esac
done

if [ "$job_name" = "" ]; then
	help
	exit 1
fi

if [ ! $(command -v wget) ]; then
	echo "Installing wget:"
	yum install -y wget
fi

if [ ! $(command -v java) ]; then
	echo "Installing java:"
	yum install -y java-1.8.0-openjdk
	export JAVA_HOME=$(command -v java)
fi

if [ ! $(command -v unzip) ]; then
	echo "Installing unzip"
	yum install -y unzip
fi

if [ ! -f fscrawler.zip ]; then
	wget "https://s01.oss.sonatype.org/content/repositories/snapshots/fr/pilato/elasticsearch/crawler/fscrawler-distribution/2.10-SNAPSHOT/fscrawler-distribution-2.10-20220225.072200-31.zip" -O fscrawler.zip
fi
if [ ! -d fscrawler-es7-2.7-SNAPSHOT ]; then
	unzip fscrawler.zip
fi
echo Copying extracted files to /opt
fscrawler_folder_location=/opt/fscrawler
if [ -d $fscrawler_folder_location ]; then
	rm $fscrawler_folder_location -rf
fi
cp -r ./fscrawler-es7-2.7-SNAPSHOT/ $fscrawler_folder_location

echo "Creating user for this service"
useradd -rms /sbin/nologin -p $password $username && echo "New system account has been added" || echo "Error while creating user."

echo "Creating service entry at systemd"
cat <<-EOF > /lib/systemd/system/fscrawler.service
	[Unit]
	Description=FSCrawler service
	After=elasticsearch
	StartLimitIntervalSec=0

	[Service]
	Restart=always
	RestartSec=1
	User=$username
	ExecStart=$fscrawler_folder_location/bin/fscrawler $job_name

	[Install]
	WantedBy=multi-user.target
EOF

echo "Starting fscrawler to create config files"
sudo -u $username $fscrawler_folder_location/bin/fscrawler $job_name

echo "Enabling fscrawler service"
/bin/systemctl daemon-reload
/bin/systemctl enable fscrawler.service

echo "Starting FSCrawler service"
systemctl start fscrawler.service

echo "Done!"
exit 0