from fastapi import FastAPI, Path, Query, Body, status, HTTPException
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest
from typing import List

# 임시 데이터베이스
users = [
    {"id": 1, "name": "alex", "age": 20},
    {"id": 2, "name": "bob", "age": 30},
    {"id": 3, "name": "chris", "age": 40},
]


app =FastAPI()

# # 서버에 GET /hello 요청이 들어오면, hello_handler를 실행한다
# @app.get("/hello")
# def hello_handler():
#     return {"ping": "pong"}




# 전체 사용자 조회 API
@app.get(
        "/users",
        status_code=status.HTTP_200_OK,
        response_model=List[UserResponse],
)
def get_users_handlers():
    return users

# 회원 검색 API
# HTTP Method: GET, POST, PUT, PATCH, DELETE
# Query Parameter
# ->  ?key=value 형태로 Path 뒤에 붙는 값
# -> 데이터 조회시 부가 조건을 명시(필터링, 정렬, 검색 ,페이지네이션 등)
@app.get(
        "/users/search",
        status_code=status.HTTP_200_OK,
        response_model=UserResponse,
)
def search_user_handler(
    # name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다
    name: str = Query(..., min_length=2),  # ... -> 필수값(required)
    age: int = Query(None, ge=1), # default 값 지정 -> 선택적(optional)
):
    return {"id":0,"name": name, "age": age}


# {user_id}번/단일 사용자 조회 API
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는지 검사  & 보장

# GET/users/1?field=id -> id 반환
# GET/users/1?field=name -> name 반환
# GET/users/1 (없으면)-> id,name 반환
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자의 ID"),
    field: str = Query(None, description="출력할 필드 선택(id 또는 name)"),
) -> UserResponse:
    if user_id > len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자의 ID입니다.",
        )
    
    user = users[user_id - 1]

    if field in ("id", "name"):
        return {field: user[field]}
    return user


    # gt : 초과
    # ge : 이상
    # lt : 미만
    # le : 이하
    # max_digits: 최대 자리수 000000


# 회원가입 API
@app.post(
        "/users/sign-up", 
        status_code=status.HTTP_201_CREATED,

        # 응답은 UserSignUpResponse 데이터 구조를 따라야한다
        # UserSignUpResponse(id:int, name:str, age: int | None)

        # 1) 서버에서 원하는 데이터 형식으로 응답이 반환되는지 검증
        # 2) 노출되면 안 되는 값을 자동으로 제거
        # 3) API 문서에 예상되는 응답 출력
        response_model=UserResponse,
)
def sign_up_handler(body: UserSignUpRequest):
    # 함수에 선언한 매개변수의 타입힌트가 BaseModel을 상속 받은 경우, 요청 본문에서 가져옴
    # 데이터 가져오면서, 타입힌트에 선언한 데이터 구조와 맞는지 검사

    # body = UserSignUpRequest(name=..., age=...)
    # body 데이터가 문제 없으면 -> 핸들러 함수로 전달
    # body 데이터가 문제 있으면 -> 즉시  실행이 멈추고, 422 에러
    
    new_user ={
        "id": len(users) + 1, "name": body.name, "age": body.age}
    users.append(new_user)
    return new_user


# 사용자 정보 수정 API
# PUT :전체업데이트-> {name, age} 한 번에 교체
# PATCH : 일부분 업데이트 -> name | age 하나씩 교체
@app.patch(
        "/users/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserResponse,
)
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),

):
    # Pseudo Code
    # 1) user_id 검증
    if user_id > len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자의 ID입니다.",
        )
    
    # 1-b) body 데이터 검증
    if body.name is None and body.age is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 데이터가 없습니다.",
        )

    # 2) 사용자 조회 & 수정
    user = users[user_id - 1]

    # A) name만 수정하는경우 -> L#132
    # B) age만 수정하는 경우 ->L#135
    # C) name, age 모두 수정하는 경우 -> L#132, L#135
    # D) name, age 모두 수정하지 않는 경우  -> 1-b처리

    if body.name is not None:
        user["name"] = body.name

    if body.age is not None:
        user["age"] = body.age

    # 3) 응답 반환
    return user






### 실습

# GET /Items/{item_name}
# item_name: str & 최대 글자수(max_length) 6
# 응답 형식: {"item_name": ...}

@app.get("/items/{item_name}")
def get_item_handler(
    item_name: str = Path(..., max_length=6),
):
    return {"item_name": item_name}
