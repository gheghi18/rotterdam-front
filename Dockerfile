FROM pierrezemb/gostatic
COPY ./dist/ /srv/http/

ENTRYPOINT ["/goStatic", "-set-basic-auth", "gradient:boost"]

