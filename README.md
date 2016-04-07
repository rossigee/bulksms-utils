# BulkSMS utils

Just a couple of scripts I put together to use BulkSMS with our Icinga monitoring system.

sms_bulksms_send.py - Sends the text from stdin to the mobile number provided as the first argument.
sms_bulksms_balance.py - Retrieves the account credit balance from BulkSMS.

Both rely on a configuration file being in place at '/etc/bulksms.conf', containing:

	```
	[api]
	username=yourbulksmslogin
	password=yourbulksmspassword
	```

To add the balance check to your Icinga/Nagios config...

	```
	define command {
		command_name    check_bulksms_balance
		command_line    /usr/local/bin/sms_bulksms_balance.py
	}
	define service {
		use                             generic-service
		host_name                       localhost
		service_description             BulkSMS credit balance
		check_command                   check_bulksms_balance
	}
	
	```

To add SMS recipients for notifications...

	```
	define command {
		command_name   notify-host-by-sms
		command_line   /usr/bin/printf "%b" "[YourCompany] ($NOTIFICATIONTYPE$) Host $HOSTALIAS$ is $HOSTSTATE$: $HOSTOUTPUT$" \
			       | /usr/local/bin/sms_bulksms_send.py $CONTACTEMAIL$
	}

	define command {
		command_name   notify-service-by-sms
		command_line   /usr/bin/printf "%b" "[YourCompany] ($NOTIFICATIONTYPE$) Service $SERVICEDESC$ on $HOSTALIAS$ is $SERVICESTATE$: $SERVICEOUTPUT$" \
			       | /usr/local/bin/sms_bulksms_send.py $CONTACTEMAIL$
	}

	define contact {
		contact_name                    fred-by-sms
		alias                           Fred (by SMS)
		service_notification_period     24x7
		host_notification_period        24x7
		service_notification_options    c
		host_notification_options       d
		service_notification_commands   notify-service-by-sms
		host_notification_commands      notify-host-by-sms
		email                           66123456789  # (Fred's mobile number)
	}
	```

