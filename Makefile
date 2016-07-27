local_dir = $(shell pwd)

build:
	docker build -t http2 .

run:
	docker run -d -v $(local_dir):/app -p 8080:8080 --name twist http2

restart:
	docker restart twist

clean:
	docker stop twist
	docker rm twist
	docker rmi http2



