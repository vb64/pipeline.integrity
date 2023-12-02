rem files to add
cp ../../requirements.txt requirements.txt
cp ../../tests/requirements.txt tests.txt
docker-compose build
rem cleanup
rm requirements.txt
rm tests.txt
