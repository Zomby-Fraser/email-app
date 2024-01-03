#!/bin/bash

# Remove the temporary Postfix config file if it exists
rm -f /etc/postfix/main.cf.tmp

# Then start Postfix normally
exec "$@"
