docker build -t ssti_1_build .
docker run -d -p 15378:8080 --name=ssti_1 ssti_1_build

