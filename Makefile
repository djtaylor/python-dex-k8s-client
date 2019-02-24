dex_version=v2_14_0
dex_docker_port=35556
dex_dockerfile=docker_files/Dockerfile_${dex_version}
dex_docker_image_name=dex-api-server
hydra_dockerfile=docker_files/Dockerfile_HydraOID
hydra_docker_image_name=hydra-oidc-server
oidc_test_client=test-client
oidc_test_secret=testsecret

build:

	# Compile protocol buffers
	venv/bin/python3 -m grpc_tools.protoc -I./proto \
	--python_out=./ \
	--grpc_python_out=./ \
	proto/dex_api_client/dexidp/dex/api/${dex_version}.proto

	# Build Dex/Hydra for functional testing
	./docker-compose.sh build

run:
	./docker-compose.sh up -d

	# Get root credentials from Hydra logs
	./oidc_client.sh

install:
	virtualenv --python python3 venv
	chmod +x venv/bin/activate
	venv/bin/pip3 install -r requirements.txt
	venv/bin/python3 setup.py install

clean:
	./docker-compose.sh down
	venv/bin/python3 setup.py clean --all

test_hydra:
	source .oidc_client && hydra connect \
		--id ${OIDC_CLIENT_ID} \
		--secret ${OIDC_CLIENT_SECRET} \
		--url

test:
	venv/bin/python3 setup.py test

logs:
	docker logs ${dex_docker_image_name}
	docker logs ${hydra_docker_image_name}
