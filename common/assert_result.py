import traceback


def check_result(data, result, logger):
    try:
        assert data == result
        logger.info(f'用例通过,返回结果:{data},预期结果:{result}')
        return True
    except AssertionError:
        logger.error(f'用例不通过,返回结果:{data},预期结果:{result}')
        logger.error(traceback.format_exc())
        print(f"data:{data}")
        print(f"result:{result}")
        return False


def check_result_is_true(data, logger):
    try:
        assert data is not None
        logger.info(f'用例通过,返回结果:{data}，不为空')
        return 1
    except AssertionError:
        logger.error(f'用例不通过,返回结果:{data}')
        logger.error(traceback.format_exc())
        return 0


def check_result_is_401(data, logger):
    result = data['error_code']
    try:
        assert result == 401
        logger.info(f'用例通过，返回结果{data}')
    except AssertionError:
        logger.error(f'用例不通过，返回结果{data},\nresult:{result}不为401')
        logger.error(traceback.format_exc())
        return 0


def check_result_is_422(data, logger):
    result = data['error_code']
    try:
        assert result == 422
        logger.info(f'用例通过，返回结果{data}')
    except AssertionError:
        logger.error(f'用例不通过，返回结果{data},\nresult:{result}不为422')
        logger.error(traceback.format_exc())
        return 0


def check_result_is_500(data, logger):
    result = data['error_code']
    try:
        assert result == 500
        logger.info(f'用例通过，返回结果{data}')
    except AssertionError:
        logger.error(f'用例不通过，返回结果{data},\nresult:{result}不为500')
        logger.error(traceback.format_exc())
        return 0


def check_res_in(res, array, logger):
    try:
        assert res in array
        logger.info(f'用例通过，res:{res},array:{array}')
    except AssertionError:
        logger.error(f'用例不通过，res:{res},array:{array}')
        logger.error(traceback.format_exc())
        return 0
