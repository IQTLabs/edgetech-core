FROM smallstep/step-cli as step
FROM eclipse-mosquitto 
LABEL maintainer = "Ryan <rashley@iqt.org>"

#copy step binary for bootstrapping ca
COPY --from=step /usr/local/bin/step /usr/local/bin/

RUN apk add --update curl mosquitto ca-certificates certbot openrc && rm -rf /var/cache/apk/*
COPY mosquitto.conf /etc/mosquitto/mosquitto.conf
# COPY server.mqtt.local.conf /etc/letsencrypt/renewal/server.mqtt.local.conf
COPY trust_ca.sh .
COPY update_mqtt_cfg.sh .
COPY start_mqtt.sh .
EXPOSE 1883
EXPOSE 8883


HEALTHCHECK --interval=15s --timeout=15s \
 CMD timeout 1 mosquitto_sub -h localhost -p 1883 -t '$SYS/#' -u $(cat /run/secrets/mqtt_user) -P $(cat /run/secrets/mqtt_pass) -E -i probe || exit 1

ENTRYPOINT ["./start_mqtt.sh"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]