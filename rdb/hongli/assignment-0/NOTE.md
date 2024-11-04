remember to add new group for docker to grant the user (rather than root)
the previlege to run docker commands:
https://docs.docker.com/engine/install/linux-postinstall/

docker run \
rddaimage \
--name mydb \
--rm \
-p 5432:5432 \
-e POSTGRES_PASSWORD="thisIsabetterPASS" \
postgres:17.0

docker run: 启动一个新的 Docker 容器。
--name mydb: 给容器指定一个名称为 "mydb"。这使得管理和识别容器更方便。
--rm: 当容器停止时，会自动删除该容器。这样可以节省资源，避免留下不必要的容器。
-p 5432:5432: 将容器内部的 5432 端口映射到主机上的 5432 端口。这是 PostgreSQL 的默认端口，因此可以从主机访问到该数据库。
-e POSTGRES_PASSWORD="chooseGoodPassword": 设置环境变量 POSTGRES_PASSWORD，为数据库的超级用户（默认是 "postgres" 用户）指定密码，这里密码是 "chooseGoodPassword"。建议使用更安全的密码。
postgres:17.0: docker image name to use to create hte container and its version.


docker exec -ti mydb bash
psql -U postgres

进入容器的交互式终端：

bash
Copy code
docker exec -ti mydb bash
docker exec: 用于在正在运行的容器中执行命令。
-ti: 表示使用交互式终端模式（-t 为分配一个伪终端，-i 为保持 STDIN 开启）。
mydb: 容器名称，这里为 mydb。
bash: 命令，表示进入容器内部的 Bash 终端。
运行该命令后，你将进入容器内部的命令行界面。

连接到 PostgreSQL 数据库：

bash
Copy code
psql -U postgres
psql: PostgreSQL 的命令行工具，用于连接和管理数据库。
-U postgres: 指定以 postgres 用户身份连接数据库。
进入 PostgreSQL 数据库后，你可以执行 SQL 查询并管理数据库。
