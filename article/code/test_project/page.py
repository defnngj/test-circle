

class LoginPage():

    def __init__(self, driver) -> None:
        self.driver = driver
    
    @property
    def username(self):
        return self.driver.find_element_by_id("user")
    
    @property
    def password(self):
        return self.driver.find_element_by_id("pawd")
