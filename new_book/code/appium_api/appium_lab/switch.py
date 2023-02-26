# appium_lab/switch.py
from loguru import logger


class Switch:
    """
    基于appium 切换上下文
    """

    def __init__(self, driver):
        self.driver = driver

    def context(self):
        """
        返回当前context.
        """
        current_context = self.driver.current_context
        all_context = self.driver.contexts
        logger.info(f"current context: {current_context}.")
        logger.info(f"all context: {all_context}.")
        return current_context

    def switch_to_app(self) -> None:
        """
        切换到原生app.
        """
        current_context = self.driver.current_context
        if current_context != "NATIVE_APP":
            logger.info("Switch to native.")
            self.driver.switch_to.context('NATIVE_APP')

    def switch_to_web(self, context_name: str = None) -> None:
        """
        切换到webview.
        """
        logger.info("Switch to webview.")
        if context_name is not None:
            self.driver.switch_to.context(context_name)
        else:
            all_context = self.driver.contexts
            for context in all_context:
                if "WEBVIEW" in context:
                    self.driver.switch_to.context(context)
                    break
            else:
                raise NameError("No WebView found.")

    def switch_to_flutter(self) -> None:
        """
        切换到flutter.
        """
        current_context = self.driver.current_context
        if current_context != "FLUTTER":
            logger.info("Switch to flutter.")
            self.driver.switch_to.context('FLUTTER')
