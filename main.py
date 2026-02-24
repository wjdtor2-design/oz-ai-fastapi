from fastapi import FastAPI, Path, Query


app =FastAPI()

# # 서버에 GET /hello 요청이 들어오면, hello_handler를 실행한다
# @app.get("/hello")
# def hello_handler():
#     return {"ping": "pong"}

users = [
    {"id": 1, "name": "alex"},
    {"id": 2, "name": "bob"},
    {"id": 3, "name": "chris"},
]


# 전체 사용자 조회 API
@app.get("/users")
def get_users_handlers():
    return users

# 회원 검색 API
# HTTP Method: GET, POST, PUT, PATCH, DELETE
# Query Parameter
# ->  ?key=value 형태로 Path 뒤에 붙는 값
# -> 데이터 조회시 부가 조건을 명시(필터링, 정렬, 검색 ,페이지네이션 등)
@app.get("/users/search")
def search_user_handler(
    # name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다
    name: str = Query(..., min_length=2),  # ... -> 필수값(required)
    age: int = Query(None, ge=1), # default 값 지정 -> 선택적(optional)
):
    return {"name": name, "age": age}


# {user_id}번/단일 사용자 조회 API
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는지 검사  & 보장

# ?field=id -> id 반환
# ?field=name -> name 반환
# 없으면 -> id,name 반환
@app.get("/users/{user_id}")
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자의 ID"),
    field: str = Query(None, description="출력할 필드 선택(id 또는 name)"),
):
    user = users[user_id - 1]
    
    if field in ("id", "name"):
        return {field: user[field]}
    return user


    # gt : 초과
    # ge : 이상
    # lt : 미만
    # le : 이하
    # max_digits: 최대 자리수 000000


### 실습

# GET /Items/{item_name}
# item_name: str & 최대 글자수(max_length) 6
# 응답 형식: {"item_name": ...}

@app.get("/items/{item_name}")
def get_item_handler(
    item_name: str = Path(..., max_length=6),
):
    return {"item_name": item_name}
