## 빌드, 배포
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
    2. 실행 오류 시 docker-compose up -d 한번 더 실행 필요
        - nginx에 depends가 되는 app이 nginx보다 늦게 실행된 경우 에러 발생


3. replica 및 샤딩 설정
    1. docker exec -it centraldb_1 mongosh 실행으로 replica셋 연동 / 이후 rs.status()로 결과 확인
        ```
                rs.initiate(
        {
            _id: "centralReplSet",
            members: [
                { _id: 0, host: "central_db1:27017" },
                { _id: 1, host: "central_db2:27017" },
                { _id: 2, host: "central_db3:27017" }
            ]
        }
        )
        ```
    2. configsvr1, shardSeoul1, shardGunsan1, shardElse1 도 똑같은 방식으로 나머지 replica와 연동
        - 단 configsvr1는 포트가 다르게 설정되어있어 docker exec -it configsvr1 mongosh --port 27019로
    3. 샤딩 설정 
        1. 샤드 추가
            ```
            sh.addShard("shardReplSetSeoul/shardSeoul1:27017,shardSeoul2:27017,shardSeoul3:27017")
            sh.addShard("shardReplSetGunsan/shardGunsan1:27017,shardGunsan2:27017,shardGunsan3:27017")
            sh.addShard("shardReplSetElse/shardElse1:27017,shardElse2:27017,shardElse3:27017")
            ```
        2. 샤딩 활성화 sh.enableSharding("ssafy")
        3. ip 주소 첫 자리 기준으로 분배해줄거라 이와 같이 샤딩키 설정 sh.shardCollection("ssafy.face_gesture_info", { "ip_first_octet": 1 })
        4. 샤딩키에 따라 자동 분배하도록 설정
            ```
            // 100 이하의 ip_first_octet은 shardReplSetElse로
            sh.addTagRange("ssafy.face_gesture_info", 
                        { "ip_first_octet": MinKey }, 
                        { "ip_first_octet": 100 }, 
                        )

            // 101 ~ 200의 ip_first_octet은 shardReplSetGunsan로
            sh.addTagRange("ssafy.face_gesture_info", 
                        { "ip_first_octet": 101 }, 
                        { "ip_first_octet": 200 }, 
                        )

            // 201 이상의 ip_first_octet은 shardReplSetSeoul로
            sh.addTagRange("ssafy.face_gesture_info", 
                        { "ip_first_octet": 201 }, 
                        { "ip_first_octet": MaxKey }, 
                        )
            ```
        5. sh.status()로 확인
## 외부 서비스 정리 문서
- 외부 서비스 정보(소셜로그인)

- Naver Login (OAuth 2.0)
인증 방식 : OAuth 2.0
필요 정보 : Client ID, Client Secret
관련 URL : https://developers.naver.com/main/

- Kakao Login (OAuth 2.0)
인증 방식 : OAuth 2.0
필요 정보 : REST API 키
관련 URL : https://developers.kakao.com/

## DB 덤프 파일 최신본
1. mainDB_dump: 유저 전체 데이터 저장
2. shardingDB_dump: 지역별 정보 저장

## 시연 시나리오 (파일위치: frontend/Xdesk)
0. frontend/XDesk main.py 실행된 상태
1. 소셜 로그인 or 얼굴 + 모션 로그인
    - 첫 화면(FirstPage.qml) 클릭으로 로그인페이지(loginPage.qml)로 이동	
    1. 소셜 로그인 
        1. 네이버 로그인 or 카카오 로그인 선택시 qr코드 페이지 오픈됨
        2. 본인의 핸드폰을 통해 qr인증시 서버에서 유저데이터 전송
        3. 결과에 따라 하단과 같이 이동
            - 얼굴 정보가 있을시 높이조절화면(deskStandAdjust.qml)으로 이동
            - 없을 시 얼굴 등록 문의 화면(AskRecogFaceID.qml)으로 이동
    
    2. 얼굴 + 모션 로그인
        1. faceID 로그인 클릭시 얼굴 인식 페이지로 이동(faceLoginPage.qml)
        2. 얼굴 인식 성공시 제스처 인식 페이지로 이동(gestureLoginPage.qml)
        3. 결과에 따라 하단과 같이 이동
            - 성공시 높이조절화면(deskStandAdjust.qml)으로 이동
            - 실패시 실패화면(faceLoginFail.qml)이 뜨고 "확인" 버튼 클릭시 로그인페이지(loginPage.qml)로 이동
    
    3. 얼굴 등록 진행
        1. 얼굴 등록 문의 화면(AskRecogFaceID.qml)에서 "얼굴 인식하기" 클릭 시 얼굴 인식 화면("faceIdSignUp.qml") 이동, "아니오 등록하지 않겠습니다" 클릭 시 메인페이지(mainPage.qml)로 이동
        2. 얼굴 등록이 완료시 제스처 제공 화면("gesture.qml")으로 이동
        3. 제스처 제공 화면에서 "확인" 버튼 클릭 시 높이조절화면(deskStandAdjust.qml)으로 이동

    4. 높이조절화면에서 높이 조정
        1. "AI 추천" 버튼 클릭 시 자세 안내 화면(aiExample.qml)로 이동 후 자동으로 높이 조절, 조절 완료 후 메인페이지(mainPage.qml)로 이동
        2. "저장소" 버튼 클릭시 기존 저장된 값들 중 하나 선택 가능, 선택 시 높이 조절 후 메인페이지(mainPage.qml)로 이동   
            - 상단 X 버튼 클릭 시 뒤로가기 
        3. "사용 안함" 버튼 클릭시 메인페이지(mainPage.qml)로 바로 이동   
    
    5. 방해금지모드
        1. "방해금지" 버튼 클릭시 버튼 css 변화되며 나머지 버튼은 비활성화됨, 재클릭시 원래 상태로 복귀
    
    6. 수동모드
        1. "수동모드" 버튼 클릭시 수동조작 화면(manualMode.qml)으로 이동
        2. 화살표 버튼을 클릭하여 책상 및 거치대 높이 조절 가능
        3. 상단 X 버튼 클릭 시 메인페이지(mainPage.qml)로 이동
    
    7. 저장소
        1. 빈 "+" 공간 클릭시 현재 책상과 거치대 높이 값 저장, 서버에 저장 request 요청
        2. 데이터가 저장된 공간 클릭 시 해당 높이로 높이 조절 후 메인페이지(mainPage.qml)로 이동 
        3. 데이터가 저장된 공간 하단의 "덮어쓰기" 클릭시 덮어쓰기, "삭제"의 경우 삭제됨
    
    8. 타이머
        1. 우측 "1분", "5분", "10분", "30분" 클릭 시 좌측 타이머 시간 증가 or 좌측 타이머를 드래그해서 시간 조정가능
        2. "시작"버튼 클릭 시 타이머 시작되며 우측 타이머가 작동
        3. 타이머 작동 시 "중지" 버튼 클릭시 타이머 일시 중지, "초기화" 버튼 클릭 시 타이머 재 설정 가능
        4. 타이머 완료시 알람 표시. "확인"버튼 클릭으로 모달 비활성화
        5. 상단 X 버튼 클릭 시 메인페이지(mainPage.qml)로 이동
    
    9. 그래프
        1. "자세 그래프" 클릭시 그래프 팝업창(ImageDialogPage.qml) 표시/ 첫번째 요청시에만 서버에 그래프 이미지 받아옴.
        2. 상단 X 버튼 클릭 시 메인페이지(mainPage.qml)로 이동
    
    10. 로그아웃
        1. 로그아웃 버튼 클릭시 첫 화면(FirstPage.qml)으로 이동

