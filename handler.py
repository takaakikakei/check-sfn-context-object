from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test(event, context):
    try:
        # タイムアウトを意図的に引き起こす処理
        sleep(30)
    except Exception as e:
        logger.exception("test {}".format(e))
        return str(e)
    else:
        return True
