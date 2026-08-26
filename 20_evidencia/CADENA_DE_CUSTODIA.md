| ID | Archivo | SHA-256 | Fecha y hora (UTC) | Obtenido por | Método de obtención | Sistema origen |
|:--:|:--------|:--------|:------------------:|:-------------|:---------------------|:---------------|
| E01-01 | E01_baseline/contenedores.json | dd8fa9584cdc592b409d86610e03460cbd69cb200cc13d5efcd6e83a0d778c35 | 2026-08-26 15:30:00 | Bruno Ancco | docker compose ps (json) | Host Docker local |
| E01-02 | E01_baseline/imagenes.tsv | f8f359f9e20dfc9fb5dd12880ec1e281131261a1415390b4c95fd2fd6a88ecb8 | 2026-08-26 15:30:00 | Bruno Ancco | docker images --digests | Host Docker local |
| E01-03 | E01_baseline/puertos.tsv | 1f221c0edd57bc23ead3800f00170872d0b9f0d7ab4e32dc0904fd6ee3cb865f | 2026-08-26 15:31:00 | Bruno Ancco | docker ps (ports) | Host Docker local |
| E01-04 | E01_baseline/compose_efectivo.yml | 3acb22e679ec95a09705b799ddeca40b1cdab5cc2cab8ec299560483b8a8c56e | 2026-08-26 15:31:00 | Bruno Ancco | docker compose config | Docker Engine |
| E01-05 | E01_baseline/usuarios_postgres.txt | 51697ec50673e8c10a7418a82486a719e9e7758905113a72f5dc95ff3469a59b | 2026-08-26 15:32:00 | Bruno Ancco | docker exec psql (\du) | Contenedor si084_db |
| E01-06 | E01_baseline/env_db.json | af32b889fbae13a312669ffa58b8881b9d6fe3176903e7ff2f8d5eedbeff5e02 | 2026-08-26 15:32:00 | Bruno Ancco | docker inspect (Env) | Contenedor si084_db |