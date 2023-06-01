#! /bin/sh

step ca bootstrap -f --ca-url https://ca:8050 --fingerprint $(curl -s http://ca:8051/fingerprint)
cp $HOME/.step/certs/root_ca.crt /usr/local/share/ca-certificates/
update-ca-certificates 2>/dev/null