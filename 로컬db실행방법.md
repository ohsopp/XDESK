# 로컬에서 실행하는 법
1. 최상위 폴더에 .env 파일 추가
```
DATABASE_URL =mongodb://central_db:27017
REGIONDB_URL =mongodb://mongos:27017 
NAVER_OAUTH_CLIENT_ID=본인 id
NAVER_OAUTH_CLIENT_SECRET=본인 secret
KAKAO_OAUTH_CLIENT_ID=본인 id
KAKAO_OAUTH_CLIENT_SECRET=본인 secret
SECRET_KEY=본인이 설정할 secretkey 아무거나 ok
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
2. 최상위 폴더에서 docker-compose up -d로 실행
    1. docker ps -a로 실행이 잘 돌아가는지 확인 가능
    2. 오류시 docker logs 안되는 파일 이름 으로 디버깅!

3. docker 설정 수정이 필요한 경우
    1. docker-compose down으로 서버 끄기
    2. docker-compose.yml 수정
    3. docker-compose up -d 로 재시작

4. 백엔드 이미지 수정이 필요한 경우
    1. 백엔드 이미지 지우기 docker rmi 백엔드 이름
        1. rmi가 안먹히는 경우, 백엔드 컨테이너 끄고 지우기 docker stop/remove 백엔드이름 
        2. 잘 지워졌는지는 docker images로 확인 가능
    2. 백엔드 이미지 수정하기
    3. 최상위 폴더에서 docker-compose up -d로 재실행

# DB 확인하는법
- http://localhost/ping/ 으로 연결 유무 확인
- docker exec -it 원하는DB이름 mongosh
- show dbs 및 여러 mongosh 명령어를 통해 확인

# 복제 및 샤딩의 경우 별도 조정 필요!