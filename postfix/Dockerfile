# Use an Ubuntu base image
FROM ubuntu:latest

# Install Postfix.
RUN apt-get update && apt-get install -y postfix

# Configure Postfix
RUN postconf -e 'relayhost = [smtp.yourisp.com]'
RUN postconf -e 'mail_spool_directory = /var/mail/'
RUN postconf -e 'mailbox_command ='
RUN postconf -e 'home_mailbox = Maildir/'

# Expose SMTP port
EXPOSE 25

# Start Postfix
CMD ["postfix", "start"]
