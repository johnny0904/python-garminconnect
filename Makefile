# 變數定義
COMPOSER = composer
PHP_ARTISAN = php artisan
PHPSTAN = "./vendor/bin/phpstan"
PHPSTAN_LEVEL = 5
INTERNAL_PATH = internal

# 指令：啟動 Laravel 服務
run:
	$(PHP_ARTISAN) serve

# 指令：運行 PHPStan 靜態分析
lint:
	$(PHPSTAN) analyse $(INTERNAL_PATH) --level $(or $(level), $(PHPSTAN_LEVEL))

# 指令：dump-autoload
dump:
	$(COMPOSER) dump-autoload

migrate:
	$(PHP_ARTISAN) migrate

migrate-pretend:
	$(PHP_ARTISAN) migrate --pretend

migrate-rollback:
	$(PHP_ARTISAN) migrate:rollback

migrate-rollback-pretend:
	$(PHP_ARTISAN) migrate:rollback --pretend

migrate-seed:
	$(PHP_ARTISAN) migrate:fresh --seed

storage-link:
	$(PHP_ARTISAN) storage:link

remove-link:
	rm public\storage

# 建立 docker image
build:
	docker compose build

# 啟動 docker compose（前景模式）
up:
	docker compose up

# 啟動 docker compose（背景模式）
up-d:
	docker compose up -d

up-in-wsl:
	wsl -e docker compose up -d

# 停止並移除 docker compose 服務
down:
	docker compose down

# 重新啟動 docker compose（先 down 再 up -d）
restart:
	docker compose down; docker compose up -d

# 進入 app 容器 bash
into-app:
	docker compose exec -it app bash

# 重設資料庫（刪除並重新建立資料庫）
reset-db:
	docker compose exec db mysql -uhealthuser -phealthpassword health -e "DROP DATABASE IF EXISTS health; CREATE DATABASE health DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 清空並重建表格（基於 models.py）
reset-tables:
	uv run python -c "from your_data.db import get_engine, Base; from your_data import models; Base.metadata.drop_all(get_engine()); Base.metadata.create_all(get_engine()); print('Tables reset successfully')"

# 匯入資料庫 SQL 檔案
import-db:
	docker compose exec -i db mysql -uhealthuser -phealthpassword health < health.sql

# 進入 db 容器執行 MySQL 查詢
db-query:
	docker compose exec db mysql -u healthuser -phealthpassword -h localhost health --default-character-set=utf8mb4

# 在 app 容器內執行 composer dump-autoload
dump-in-app:
	docker compose exec app composer dump-autoload	

# 在 app 容器內執行 migrate
migrate-in-app:
	docker compose exec app php artisan migrate

# 在 app 容器內執行 seed
seed-in-app:
	docker compose exec app php artisan db:seed

# 在 app 容器內重建 table 並執行 seed
migrate-seed-in-app:
	docker compose exec app php artisan migrate:fresh --seed

# 在 app 容器內執行 composer install
composer-install-in-app:
	docker compose exec app composer install

# 追蹤 app 容器即時日誌
logs-app:
	docker compose logs -f app