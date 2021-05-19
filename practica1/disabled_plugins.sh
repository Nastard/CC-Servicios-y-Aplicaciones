#!/bin/bash
array=$(docker ps|grep nextcloud_ccsa45604264|awk '{print $1;}')
for element in $array
do
   echo "Container ${element}"
	docker exec -u 33 -it ${element} php occ app:disable accessibility dashboard accessibility firstrunwizard nextcloud_announcements photos weather_status user_status survey_client support recommendations updatenotification
done
