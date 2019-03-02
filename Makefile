dex_version=v2_14_0
dex_docker_port=35556
dex_dockerfile=docker_files/Dockerfile_${dex_version}
dex_docker_image_name=dex-api-server
hydra_dockerfile=docker_files/Dockerfile_HydraOID
hydra_docker_image_name=hydra-oidc-server
oidc_test_client=test-client
oidc_test_secret=testsecret
python_bin=venv/bin/python3
pip_bin=venv/bin/pip3

build:

	# Compile protocol buffers
	${python_bin} -m grpc_tools.protoc -I./proto \
	--python_out=./ \
	--grpc_python_out=./ \
	proto/dex_k8s_client/dexidp/dex/api/${dex_version}.proto

	# Build Dex/OpenLDAP for functional testing
	./docker-compose.sh build

run:
	./docker-compose.sh up -d

setup:
	virtualenv --python python3 venv
	chmod +x venv/bin/activate

install:
	${pip_bin} install -r requirements.txt
	${python_bin} setup.py install

clean:
	./docker-compose.sh down --remove-orphans
	${python_bin} setup.py clean --all

healthchecks:
	docker inspect --format "{{json .State.Health }}" dex-openldap | jq

debug:
	./debug.sh

test:
	${python_bin} setup.py test

test_k8s_integration:
	${python_bin} tests/k8s_integration.py

logs:
	docker logs ${dex_docker_image_name}
	docker logs dex-openldap

# Publish a release to PyPi
# NOTE: This depends on having a correctly configured ~/.pypirc
# NOTE: https://docs.python.org/3.7/distutils/packageindex.html
release:
	${python_bin} setup.py sdist bdist_wheel
	${python_bin} -m twine upload dist/*
