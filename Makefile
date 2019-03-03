dex_version=v2_14_0
dex_docker_port=35556
dex_dockerfile=docker_files/Dockerfile_${dex_version}
dex_docker_image_name=dex-api-server
python_bin=venv/bin/python3
pip_bin=venv/bin/pip3
nosetests_bin=venv/bin/nosetests

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

test: test_unit test_integration

test_unit:
	${python_bin} setup.py test

test_integration:
	${nosetests_bin} tests/integration.py

logs:
	docker logs ${dex_docker_image_name}
	docker logs dex-openldap

# Publish a release to PyPi
# NOTE: This depends on having a correctly configured ~/.pypirc
# NOTE: https://docs.python.org/3.7/distutils/packageindex.html
release:
	${python_bin} setup.py sdist bdist_wheel
	${python_bin} -m twine upload dist/*
