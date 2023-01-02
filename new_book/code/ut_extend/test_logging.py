from extends.color_logging import MyLog

log = MyLog(__name__)

log.debug("this is debug")
log.info("this is info")
log.warning("this is warning")
log.error("this is error")
log.critical("this is critical")
