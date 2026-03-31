from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import Parser
from Parser import Parser
 
 
def getDifficultyFromSudokuCoach(puzzle_str: str, headless: bool = True) -> dict:
    url = f"https://sudoku.coach/fr/solver/{puzzle_str}"
   
    #configuration du driver pour eviter les crashes et les blocages car il peut y avoir la detection de bot.
   
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    options.add_argument("-- lang=fr")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
 
    score, label = None, None
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
 
        # Accepte les cookies si le bandeau apparaît car il peut bloquer le solver JS et obstruer les résultats
        for sel in ["//button[contains(text(), 'PERMETTRE')]", "//button[contains(text(), 'Accepter')]"]:
            try:
                btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, sel)))
                btn.click()
                time.sleep(1)
                break
            except Exception:
                continue
 
        time.sleep(6)  # Laisse le solver JS tourner
        # Récupère le texte de la page pour extraire la difficulté et le score
        page_text = driver.find_element(By.TAG_NAME, "body").text
        score, label = findDifficulty(page_text)
 
    except Exception:
        pass
    finally:
        driver.quit()
 
    return {"score": score, "label": label}
 
 
def findDifficulty(page_text: str) -> tuple:
    #Cherche une ligne du type "Difficulté : <label>\n<score>" pour extraire le score et le label de difficulté dans le texte de la page
    match = re.search(r'Difficulté\s*:\s*\n([^\n]+)\n\((\d+)\)', page_text) 
    if match:
        return int(match.group(2)), match.group(1).strip()#score, label
    return None, None
 
 
def getDifficultyFromGrille(grille, headless: bool = True) -> dict:
    puzzle_str = Parser.grilleToString_v2(grille)
    return getDifficultyFromSudokuCoach(puzzle_str, headless)
 
 