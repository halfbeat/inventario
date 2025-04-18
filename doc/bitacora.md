# Cosas a no olvidar

## Montar un volumen docker por NFS

```sh
docker volume create --driver local --opt type=nfs --opt \
o="addr=192.168.1.160,rw" --opt device=":/mnt/nfsshare/volume_nfs_inventario" \
volume_inventario
```

## Crear secretos para nginx

```aiignore
docker secret create secret_inventario_nginx_key gatewayserver.key

docker secret create secret_inventario_nginx_crt gatewayserver.crt

docker secret create secret_inventario_nginx_pass gatewayserver.pass

# Create dummy secret
echo "<<< Creating dummy secret >>>" 
docker secret create dummy_key nginx.key
docker secret create dummy_crt nginx.crt

# Delete old certificate and key from docker secret and replace them with dummy
echo "<<< Delete old certificate and key from service and replace them with dummy >>>" 
docker service update \
    --secret-rm ${stack}_nginx_key \
    --secret-rm ${stack}_nginx_cert \
    --secret-add source=dummy_key,target=/etc/nginx/nginx.key \
    --secret-add source=dummy_crt,target=/etc/nginx/nginx.crt \
    ${stack}_ingress_nginx
    
echo "<<< Delete old certificate from secrets >>>"
docker secret rm  ${stack}_nginx_key
docker secret rm  ${stack}_nginx_cert

# Deploy service with new secrets
echo "<<< Create secret with new certificate and update service >>>"
docker stack deploy --compose-file docker-compose.yml $stack

# Delete dummy secrets
echo "<<< Delete dummy certificate >>>"
docker secret rm dummy_key
docker secret rm dummy_crt
```