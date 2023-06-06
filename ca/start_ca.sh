#! /bin/sh

step ca init --deployment-type standalone --name "$STEPCA_INIT_NAME}" \
--dns "${STEPCA_INIT_DNS_NAMES}" \
--address "${STEPCA_INIT_ADDRESS}" \
--provisioner "${STEPCA_INIT_PROVISIONER_NAME}" \
--password-file "${STEPCA_INIT_PASSWORD_FILE}" \
--acme

jq -r '.fingerprint' /home/step/config/defaults.json >> /static/fingerprint

nginx -g "daemon off;" &

export CONFIGPATH="/home/step/config/ca.json"
exec step-ca --password-file $STEPCA_INIT_PASSWORD_FILE $CONFIGPATH