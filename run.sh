#!/usr/bin/env bash
#
# Set up Nginx and Authelia docker images

# Unofficial bash strict mode
# set -euo pipefail
set -eu

# Change to the directory of this script
pushd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null

# Configure Nginx
nginx_certs_dir=nginx/certs
nginx_secrets_dir=nginx/secrets
mkdir -p "${nginx_certs_dir}" "${nginx_secrets_dir}"

if ! [[ -f "${nginx_certs_dir}/self-signed.crt" ]] || ! [[ -f "${nginx_secrets_dir}/self-signed.key" ]]; then
    echo 'Generating self-signed certificate...'
    openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -sha256 -keyout "${nginx_secrets_dir}/self-signed.key" -out "${nginx_certs_dir}/self-signed.crt"
fi

# Configure Authelia
authelia_db_dir=authelia/db
authelia_secrets_dir=authelia/secrets
mkdir -p "${authelia_db_dir}" "${authelia_secrets_dir}"

if ! [[ -f "${authelia_db_dir}/users.yaml" ]]; then
    touch "${authelia_db_dir}/users.yaml"
fi
if ! [[ -f "${authelia_db_dir}/main.sqlite3" ]]; then
    touch "${authelia_db_dir}/main.sqlite3"
fi

if ! [[ -f "${authelia_secrets_dir}/jwt_secret" ]]; then
    tr -dc 'A-Za-z0-9' </dev/urandom | head -c 64 >"${authelia_secrets_dir}/jwt_secret"
fi
if ! [[ -f "${authelia_secrets_dir}/notifier_smtp_password" ]]; then
    read -srp $'\n'"Please enter the value for notifier_smtp_password: " _answer
    echo "${_answer}" >"${authelia_secrets_dir}/notifier_smtp_password"
    echo
    unset _answer
fi
if ! [[ -f "${authelia_secrets_dir}/storage_encryption_key" ]]; then
    tr -dc 'A-Za-z0-9' </dev/urandom | head -c 64 >"${authelia_secrets_dir}/storage_encryption_key"
fi

# Configure File Browser
filebrowser_db_dir=filebrowser/db
mkdir -p "${filebrowser_db_dir}"

if ! [[ -f "${filebrowser_db_dir}/main.db" ]]; then
    touch "${filebrowser_db_dir}/main.db"
    podman run -v "./${filebrowser_db_dir}/main.db:/var/lib/filebrowser/main.db:rw" filebrowser/filebrowser -d /var/lib/filebrowser/main.db config init --auth.method=noauth >/dev/null
    podman run -v "./${filebrowser_db_dir}/users.yaml:/etc/filebrowser/users.yaml:ro" -v "./${filebrowser_db_dir}/main.db:/var/lib/filebrowser/main.db:rw" filebrowser/filebrowser -d /var/lib/filebrowser/main.db users import /etc/filebrowser/users.yaml >/dev/null
    podman run -v "./${filebrowser_db_dir}/config.yaml:/etc/filebrowser/config.yaml:ro" -v "./${filebrowser_db_dir}/main.db:/var/lib/filebrowser/main.db:rw" filebrowser/filebrowser -d /var/lib/filebrowser/main.db config import /etc/filebrowser/config.yaml >/dev/null
fi

# Build docker images
podman-compose up
