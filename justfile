# To install just on a per-project basis
# 1. Activate your virtual environemnt
# 2. uv add --dev rust-just
# 3. Use just within the activated environment

#drive_uuid := "77688511-78c5-4de3-9108-b631ff823ef4"
drive_uuid := "8425-155D"

user :=  file_stem(home_dir())
def_drive := join("/media", user, drive_uuid)
project := file_stem(justfile_dir())
local_env := join(justfile_dir(), ".env")


# list all recipes
default:
    just --list

init:
    uv sync

# Install tools globally
tools:
    uv tool install twine
    uv tool install ruff

# Build the package
build:
    rm -fr dist/*
    uv build



# Backup .env to storage unit
env-bak drive=def_drive: (check_mnt drive) (env-backup join(drive, "env", project))

# Restore .env from storage unit
env-rst drive=def_drive: (check_mnt drive) (env-restore join(drive, "env", project))

# -------------------
# Databases and tools
# -------------------

# New Auth database
authnew verbose="":
    uv run nx-auth-schema --console --log-file nixnox.log {{ verbose }}
    #uv run nx-auth-admin --console --trace {{ verbose }} create -l admin -p 1234 -r admin -f "Admin User"

# Populate auth database
authusers verbose="":
     uv run nx-auth-admin --console --trace {{ verbose }} create -l foo -p 1234 -r user -f The_Foo_User
     uv run nx-auth-admin --console --trace {{ verbose }} list --all
     uv run nx-auth-admin --console --trace {{ verbose }} delete -l foo
     uv run nx-auth-admin --console --trace {{ verbose }} list -l admin
     uv run nx-auth-admin --console --trace {{ verbose }} update -l admin -k -r admin -f Admin_User
     uv run nx-auth-admin --console --trace {{ verbose }} list --all

# New NIXNOX database  
nxnew verbose="":
    uv run nx-db-schema --console --log-file nixnox.log {{ verbose }}
    uv run nx-db-populate --console --trace --log-file nixnox.log {{ verbose }} all --batch-size 25000
   

# Start all databases afresh  
anew verbose="": (authnew verbose) (nxnew verbose)
   

# Starts a new SQLD database export migration cycle
# we need to add 127.0.0.1 *.db.sarna.dev to /etc/local/hosts
# and NIXNOX_DB_URL=sqlite+libsql://nixnox.db.sarna.dev:8080
anew2 env="devel":
    #!/usr/bin/env bash
    set -exuo pipefail
    env={{env}}
    uv sync --reinstall
    curl -X DELETE http://localhost:8082/v1/namespaces/${env}
    curl -X POST http://localhost:8082/v1/namespaces/${env}/create -d '{}' -H "Content-Type: application/json" 
    uv run nx-db-schema --console --log-file nixnox.log
    uv run nx-db-populate --console --trace --log-file nixnox.log all --batch-size 25000

# ========================= #
# QUCK COMMAND LINE TESTING #
# ========================= #

load:
    #!/usr/bin/env bash   
    set -exuo pipefail
    uv run nx-obs-load --console --trace observation --input-file TASD4B_AS_2024-10-23_224926_CASLEO.ecsv --text TASD4B_AS_2024-10-23_224926_CASLEO.txt
    uv run nx-obs-load --console --trace observation --input-file TASF46_AS_2024_10_05_042321_Yela.ecsv --text TASF46_AS_2024_10_05_042321_Yela.txt

import:
    #!/usr/bin/env bash   
    set -exuo pipefail
    uv run nx-db-import --console --verbose --trace all --folder export

export:
    #!/usr/bin/env bash   
    set -exuo pipefail
    uv run nx-db-export --console --verbose --trace all --folder export

# ==================== #
# NIXNOX HTTP API TEST #
# ==================== #

api:
    uv run nx-api-server --console --verbose --trace

hello:
    curl -X GET http://localhost:8086/v1
   
# ============================== #
# NIXNOX WEB TEST AND PROTOTYPES #
# ============================== #

webo:
    #!/usr/bin/env bash   
    set -exuo pipefail
    NX_ENV=dev uv run streamlit run packages/nixnox-web/web_app.py --logger.level=debug

web:
    #!/usr/bin/env bash   
    set -exuo pipefail
    NX_ENV=dev uv run nixnox-web

# Starts LibSQL sqld server: debug|release
sqld target="debug":
    #!/usr/bin/env bash   
    set -exuo pipefail
    SQLD_NODE=primary ./sqld-{{target}} --db-path ../data.sqld --no-welcome --disable-metrics \
    --admin-listen-addr 127.0.0.1:8082 --enable-namespaces


# =============
# PyTest driver
# =============

test pkg async module:
    uv run pytest packages/nixnox-api/tests/{{pkg}}/{{async}}/test_{{module}}.py

testf pkg async module func:
    uv run pytest packages/nixnox-api/tests/{{pkg}}/{{async}}/test_{{module}}.py::test_{{func}}


# =======================================================================

    

[private]
check_mnt mnt:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ ! -d  {{ mnt }} ]]; then
        echo "Drive not mounted: {{ mnt }}"
        exit 1 
    fi

[private]
env-backup bak_dir:
    #!/usr/bin/env bash
    set -exuo pipefail
    if [[ ! -f  {{ local_env }} ]]; then
        echo "Can't backup: {{ local_env }} doesn't exists"
        exit 1 
    fi
    mkdir -p {{ bak_dir }}
    cp {{ local_env }} {{ bak_dir }}
    cp nixnox.db {{ bak_dir }}
    cp *.ecsv {{ bak_dir }}
    cp *.txt {{ bak_dir }}
    cp -r .streamlit {{ bak_dir }}
    # This is experimental LibSQL Daemon
    [ ! -f {{ bak_dir }}/sqld-debug ] && cp sqld-debug {{ bak_dir }}
    [ ! -f {{ bak_dir }}/sqld-release ] && cp sqld-release {{ bak_dir }}
    cp -r data.sqld {{ bak_dir }}
  
[private]
env-restore bak_dir:
    #!/usr/bin/env bash
    set -euxo pipefail
    if [[ ! -f  {{ bak_dir }}/.env ]]; then
        echo "Can't restore: {{ bak_dir }}/.env doesn't exists"
        exit 1 
    fi
    cp {{ bak_dir }}/.env {{ local_env }}
    cp {{ bak_dir }}/nixnox.db .
    cp {{ bak_dir }}/*.ecsv .
    cp {{ bak_dir }}/*.txt .
    cp -r {{ bak_dir }}/.streamlit .
    # This is experimental LibSQL Daemon
    [ -f sqld-release ] && cp {{ bak_dir }}/sqld-release .
    [ -f sqld-debug ] && cp {{ bak_dir }}/sqld-debug .
    cp -r {{ bak_dir }}/data.sqld .
