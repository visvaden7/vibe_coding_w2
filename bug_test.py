# This file contains an intentional runtime error to test the issue management workflow.

def intentional_runtime_error_function():
    print("This function will cause a runtime error")
    # result = 1 / 0 # ZeroDivisionError 발생 (주석 처리하여 수정)
    print("Runtime error fixed!")

# 함수 호출 (테스트 워크플로우에서 이 파일을 실행할 경우 에러가 발생하도록)
intentional_runtime_error_function()
