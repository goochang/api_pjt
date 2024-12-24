### Django DRF Project
> 작업 완료일 : 2024/12/25
- 개요: Postman 테스트를 기반으로 제작된 django DRF 프로젝트입니다.

### API 명세서  
![image](https://github.com/user-attachments/assets/12f563bc-d04b-4f27-a212-ee4a9c49526f)

- 회원가입(POST) : /api/accounts  
    username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력 / 성별, 자기소개 생략 가능  
    ![image](https://github.com/user-attachments/assets/f8dd394a-a770-4320-80b9-312ced5346a1)  
- 로그인(POST) : /api/accounts/login  
    로그인 성공시 Token발급  
    ![image](https://github.com/user-attachments/assets/90711a19-909e-4276-a9c0-94b6f88481be)  
- 프로필 조회(GET) : /api/accounts/<str:username>  
    로그인 한 사용자만 프로필 조회 가능  
    ![image](https://github.com/user-attachments/assets/6598a874-96d6-40bf-a636-c51b524801f4)  
- 프로필 수정(PUT) : /api/accounts/<str:username>  
    - 이메일, 이름, 닉네임, 생일 필수 입력 / 성별, 자기소개 생략 가능  
    - 로그인 한 사용자만 본인 프로필 수정 가능. 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안 됨.  
    ![image](https://github.com/user-attachments/assets/5dbdff4c-3a2e-4525-ae11-0d038cb32cff)  
- 프로필 탈퇴(DELETE) : /api/accounts/  
    비밀번호 확인 후 계정 삭제.  
    ![image](https://github.com/user-attachments/assets/c6eb9a6d-d9f9-41ae-ab88-8cb6dd89c556)  
- 로그아웃(POST) : /api/accounts/logout/  
    RefreshToken 토큰을 블랙리스트에 추가  
    ![image](https://github.com/user-attachments/assets/3cfb3249-fa4c-4c04-8a71-c93172112308)  
- 패스워드 변경(DELETE) : /api/accounts/  
    기존 패스워드와 변경할 패스워드는 상이해야 함  
    ![image](https://github.com/user-attachments/assets/25aec8f0-9980-4bd8-b525-3da17dbcb7f2)  
- 상품 등록(POST) : /api/products  
    ![image](https://github.com/user-attachments/assets/f118c4f6-8b54-4df8-a847-3ba81da62e90)
- 상품 목록 조회(GET) :/api/products  
    10개씩 페이지네이션으로 반환
    ![image](https://github.com/user-attachments/assets/07286eb5-8892-4205-bc58-79bb4618a6d1)  
- 상품 수정(PUT) : /api/products/<int:productId>  
    ![image](https://github.com/user-attachments/assets/0782e6cf-3e87-4f05-81da-1dd2bf94ee49)
- 상품 삭제(DELETE) : /api/products/<int:productId>  
    ![image](https://github.com/user-attachments/assets/1317f6e9-3115-4d20-a542-526e5737d089)



### PostMan 설정
1. 환경변수 설정
    ![image](https://github.com/user-attachments/assets/d46264a4-05fe-46ac-a0bb-132f0bc92cf2)

2. 로그인시 환경변수 자동 입력  
   ![image](https://github.com/user-attachments/assets/b123f1ce-a320-4da9-8728-0795e4252f77)

3. 로그인 토큰 사용  
   ![image](https://github.com/user-attachments/assets/f9c97395-00fa-44b4-96a3-9a55ae5b2aa0)

5. 로그아웃시 refreshToken 설정  
   ![image](https://github.com/user-attachments/assets/f5d26518-7c47-4535-8156-39ac8ee8755e)



