from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class JobApplicationPage:
    URL = "https://proleed.academy/exercises/selenium/online-job-application-form.php"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located((By.ID, "name")))

    def enter_name(self, name: str):
        el = self.driver.find_element(By.ID, "name")
        el.clear()
        el.send_keys(name)

    def enter_email(self, email: str):
        el = self.driver.find_element(By.ID, "email")
        el.clear()
        el.send_keys(email)

    def enter_phone(self, phone: str):
        el = self.driver.find_element(By.ID, "phone")
        el.clear()
        el.send_keys(phone)

    def select_position(self, position: str):
        Select(self.driver.find_element(By.NAME, "position")).select_by_visible_text(position)

    def set_employment_status(self, status_id: str = "employed"):
        el = self.wait.until(EC.presence_of_element_located((By.ID, status_id)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, status_id))).click()
            return
        except Exception:
            pass

        try:
            ActionChains(self.driver).move_to_element(el).click(el).perform()
            return
        except Exception:
            pass

        self.driver.execute_script("arguments[0].click();", el)

    # ✅ THIS is the missing method your test is calling




    # If hidden, make visible (many sites hide the input behind a button)

    def select_platform(self, platform: str):
        # Platform options on the site: Google Search / Online Advertisement / Friend Recommendation / Other
        Select(self.driver.find_element(By.NAME, "platform")).select_by_visible_text(platform)

    def submit(self):        return True

        btn = self.wait.until(EC.presence_of_element_located((By.ID, "add")))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "add"))).click()
            return
        except Exception:
            pass

        try:
            ActionChains(self.driver).move_to_element(btn).click(btn).perform()
            return
        except Exception:
            pass

        self.driver.execute_script("arguments[0].click();", btn)

    # ✅ THIS is the missing method your test is calling
    def upload_resume(self, file_path: str):
        """
        Upload resume by sending absolute file path to the <input type='file'> element.
        """

        from pathlib import Path

        p = Path(file_path).expanduser()
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()

        if not p.exists():
            raise FileNotFoundError(f"Resume file not found: {p}")

        # Prefer the known id if it exists on your site
        try:
            el = self.wait.until(EC.presence_of_element_located((By.ID, "resume")))
        except Exception:
            candidates = [
                (By.CSS_SELECTOR, "input[type='file']"),
                (By.CSS_SELECTOR, "input[type='file'][name*='resume' i]"),
                (By.CSS_SELECTOR, "input[type='file'][id*='resume' i]"),
                (By.CSS_SELECTOR, "input[type='file'][accept*='pdf' i]"),
            ]

            el = None
            for loc in candidates:
                try:
                    el = self.wait.until(EC.presence_of_element_located(loc))
                    if el:
                        break
                except Exception:
                    continue

            if not el:
                raise RuntimeError("Could not find a file upload input (<input type='file'>) on the page.")

        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        except Exception:
            pass

        try:
            self.driver.execute_script(
                "arguments[0].style.display='block'; arguments[0].style.visibility='visible';",
                el
            )
        except Exception:
            pass

        el.send_keys(str(p))
        return str(p)

