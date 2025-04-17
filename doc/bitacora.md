# Cosas a no olvidar

## Montar un volumen docker por NFS

```sh
docker volume create --driver local --opt type=nfs --opt \
o="addr=192.168.1.160,rw" --opt device=":/mnt/nfsshare/volume_nfs_inventario" \
volume_inventario
```