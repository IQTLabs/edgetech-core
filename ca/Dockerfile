FROM smallstep/step-ca
LABEL maintainer = "Ryan <rashley@iqt.org>"

USER root
RUN apk add --update nginx jq
RUN mkdir /static && chown step:step /static && \
    chown -R step:step /var/lib/nginx && \
    chown -R step:step /var/log/nginx && \
    chown -R step:step /run/nginx && \
    chmod +x /entrypoint.sh

HEALTHCHECK --interval=15s --timeout=15s \
 CMD curl --silent --fail http://localhost:8051/fingerprint || exit 1

USER step
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./start_ca.sh /
ENTRYPOINT ["/start_ca.sh"]