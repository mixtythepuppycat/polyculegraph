venv/bin/python:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

install: requirements.txt
	virtualenv venv
	venv/bin/pip install -r requirements.txt

.PHONY: run
run: venv/bin/python
	 venv/bin/python bot.py

major_version = $(shell sed -n -e 's/^\s*major\s*=\s*//p' docker-config.ini)
minor_version = $(shell sed -n -e 's/^\s*minor\s*=\s*//p' docker-config.ini)
patch_version = $(shell sed -n -e 's/^\s*patch\s*=\s*//p' docker-config.ini)
registry = $(shell sed -n -e 's/^\s*registryname\s*=\s*//p' docker-config.ini)

docker-build-tag: docker-config.ini
	docker build -t $(registry)/polyculegraph:$(major_version).$(minor_version).$(patch_version) .
	docker push $(registry)/polyculegraph:$(major_version).$(minor_version).$(patch_version)
	
.PHONY: tailwind
tailwind:
	npx @tailwindcss/cli -i ./static/css/styles.css -o ./static/css/output.css --watch