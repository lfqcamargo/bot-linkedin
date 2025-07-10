import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from src.models.postgres.interfaces.users_repository_interface import UsersRepositoryInterface
from src.models.postgres.entities.user import User

class LinkedinService:
    def __init__(self, user_repository: UsersRepositoryInterface) -> None:
        self.user_repository = user_repository
        self.__webdriver: webdriver.Chrome = None
        self.__user: User
    
    def execute(self, user_id: int) -> None:
        self.__user = self.user_repository.find_by_user_id(user_id)
        if self.__user is None:
            raise ValueError("Usuário não encontrado.")

        self.__open_linkedin()
        self.__log_in()
        self.__access_jobs()
        self.__browse_jobs()
        
    
    def __open_linkedin(self) -> None:
        self.__webdriver = webdriver.Chrome()
        self.__webdriver.get("https://www.linkedin.com/")
        self.__webdriver.maximize_window()
        time.sleep(2)
        
    def __log_in(self) -> None:
        self.__webdriver.find_element(By.LINK_TEXT, "Entrar").click()
        time.sleep(2)
        form_login = self.__webdriver.find_element(By.CLASS_NAME, "login__form")
        form_login.find_element(By.ID, "username").send_keys(self.__user.email)
        time.sleep(1)
        form_login.find_element(By.ID, "password").send_keys(self.__user.password)
        time.sleep(1)

        form_login.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait confirmation 10 minutes
        WebDriverWait(self.__webdriver, 600).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )
        
        
    def __access_jobs(self) -> None:
        self.__webdriver.find_element(By.CSS_SELECTOR, "a[href*='jobs']").click()
        WebDriverWait(self.__webdriver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "jobs-home-vertical-list__entity-list")
            )
        )
        div_a = self.__webdriver.find_element(
            By.CLASS_NAME, "discovery-templates-vertical-list__footer"
        )
        div_a.find_element(By.TAG_NAME, "a").click()

        # Wait load
        WebDriverWait(self.__webdriver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "scaffold-layout__list-detail-container")
            )
        )

        time.sleep(2)
        self.__webdriver.find_element(By.XPATH, "//a[text()='Candidatura simplificada']").click()
        time.sleep(4)
        
    def __browse_jobs(self) -> None:
        jobs = self.__webdriver.find_elements(
            By.CSS_SELECTOR,
            ".scaffold-layout__list > div > ul > li",
        )
        
        for job in jobs:
            div_job = job.find_element(By.TAG_NAME, "div")
            self.__webdriver.execute_script(
                "arguments[0].scrollIntoView();", div_job
            )
            div_job.find_element(By.TAG_NAME, "div").click()
            time.sleep(2)
            
            self.__apply_job()
            
        try:
            next_button = self.__webdriver.find_element(
                By.CSS_SELECTOR,
                'button.jobs-search-pagination__button--next'
            )

            next_button.click()
            self.__browse_jobs()
        except Exception as e:
            print(e)
            
            
    def __apply_job(self) -> None:
        try:
            WebDriverWait(self.__webdriver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-apply-button--top-card")
                )
            ).find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
            
            try :                
                self.__fill_contact_information()
                self.__select_curriculum()            
            except Exception as e:
                self.__close_job()
            
            try:
                self.__webdriver.find_element(By.XPATH, "//span[text()='Enviar candidatura']").click()
                time.sleep(2)
                self.__webdriver.find_element(By.XPATH, "//span[text()='Concluído']").click()
                time.sleep(2)
            except Exception as e:
                self.__close_job()
        except Exception as e:
            print(e)
            
            
    def __fill_contact_information(self) -> None:
        divs_input = self.__webdriver.find_elements(
            By.CSS_SELECTOR, "div[data-test-text-entity-list-form-component]"
        )

        select_email = divs_input[0].find_element(By.TAG_NAME, "select")
        select = Select(select_email)
        select.select_by_value(self.__user.email)

        select_country_code = divs_input[1].find_element(By.TAG_NAME, "select")
        select = Select(select_country_code)
        for option in select.options:
            if "55" in option.get_attribute("value"):
                option.click()
                break

        input_cellphone = self.__webdriver.find_element(
            By.CSS_SELECTOR,
            "div[data-test-single-line-text-form-component][data-live-test-single-line-text-form-component]",
        )

        input_cellphone = self.__webdriver.find_element(By.TAG_NAME, "div")
        input_cellphone = self.__webdriver.find_element(By.TAG_NAME, "div")
        input_cellphone = self.__webdriver.find_element(By.TAG_NAME, "input")
        input_cellphone.clear()
        input_cellphone.send_keys(self.__user.phone)

        footer = self.__webdriver.find_element(By.TAG_NAME, "footer")
        footer = footer.find_element(
            By.CLASS_NAME, "display-flex.justify-flex-end.ph5.pv4"
        )
        footer.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
    def __select_curriculum(self) -> None:
        label = WebDriverWait(self.__webdriver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".jobs-document-upload-redesign-card__toggle-label.t-bold",
                )
            )
        )
        radio_button = label.find_element(
            By.XPATH, "./preceding-sibling::input[@type='radio']"
        )
        if not radio_button.is_selected():
            label.click()

        WebDriverWait(self.__webdriver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view",
                )
            )
        ).click()
        time.sleep(2)
        
    def  __close_job(self) -> None:
        self.__webdriver.find_element(By.XPATH, "//button[@aria-label='Fechar']").click()
        time.sleep(2)
        self.__webdriver.find_element(By.XPATH, "//span[text()='Descartar']").click()
        time.sleep(2)
        print(e)    
    
    