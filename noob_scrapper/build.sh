docker build -t noob_scrapper_build .
docker run -d -p 31337:8080 --name=noob_scrapper noob_scrapper_build
