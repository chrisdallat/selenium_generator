import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScriptGenerator:
    def generate_script(self, browser, url, actions):
        script = ""
        script += "from selenium import webdriver\n"
        script += "from selenium.webdriver.common.by import By\n"
        script += "from selenium.webdriver.support.ui import WebDriverWait\n"
        script += "from selenium.webdriver.support import expected_conditions as EC\n"
        script += f"driver = webdriver.{browser}()\n"
        script += f"driver.get('{url}')\n"

        for action in actions:
            action_type, xpath, value = action
            if action_type == "click":
                script += f"wait = WebDriverWait(driver, 10)\n"
                script += f"element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                script += f"element.click()\n"
            elif action_type == "type":
                script += f"wait = WebDriverWait(driver, 10)\n"
                script += f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                script += f"element.send_keys('{value}')\n"
            elif action_type == "input":
                script += f"wait = WebDriverWait(driver, 10)\n"
                script += f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                script += f"element.clear()\n"
                script += f"element.send_keys('{value}')\n"
            elif action_type == "submit":
                script += f"wait = WebDriverWait(driver, 10)\n"
                script += f"element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                script += f"element.submit()\n"

        script += "driver.quit()"
        return script

class SeleniumScriptGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selenium Script Generator")

        self.script_generator = ScriptGenerator()

        browser_label = tk.Label(root, text="Select a Browser:")
        browser_label.pack()

        self.browser_var = tk.StringVar()
        self.browser_var.set("Firefox")  # Default selection
        browser_option = ttk.Combobox(root, textvariable=self.browser_var, values=["Chrome", "Firefox"])
        browser_option.pack()

        url_label = tk.Label(root, text="URL:")
        url_label.pack()

        self.url_entry = tk.Entry(root)
        self.url_entry.pack()

        actions_label = tk.Label(root, text="Actions (One per line in format 'action|XPath|Value'):")
        actions_label.pack()

        self.actions_text = tk.Text(root, height=10, width=50)
        self.actions_text.pack()

        generate_button = tk.Button(root, text="Generate Script", command=self.generate_and_run_script)
        generate_button.pack()

        self.generated_script = tk.Text(root, height=10, width=50)
        self.generated_script.pack()

    def generate_and_run_script(self):
        selected_browser = self.browser_var.get()
        url = self.url_entry.get()
        actions_text = self.actions_text.get("1.0", tk.END).strip()
        action_lines = [line.split('|') for line in actions_text.split('\n') if line.strip()]
        
        actions = []

        for action in action_lines:
            action_type = action[0].strip() if len(action) > 0 else ""
            xpath = action[1].strip() if len(action) > 1 else ""
            value = action[2].strip() if len(action) > 2 else ""
            actions.append((action_type, xpath, value))

        if selected_browser and url and actions:
            script = self.script_generator.generate_script(selected_browser, url, actions)
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert(tk.END, script)
            # self.root.quit()  # Exit the GUI
            exec(script)  # Run the generated script
        else:
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert(tk.END, "Please select a browser, enter a URL, and define actions.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeleniumScriptGeneratorApp(root)
    root.mainloop()
