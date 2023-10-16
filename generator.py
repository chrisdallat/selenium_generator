import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScriptGenerator:
    DEFAULT_BROWSER = "Firefox"
    DEFAULT_WAIT = 5

    def generate_script(self, browser, url, actions):
        script = self._generate_import_statements()
        script += f"driver = webdriver.{browser}()\n"
        script += f"driver.get('{url}')\n"
        script += self._generate_actions(actions)
        script += "time.sleep(5)\n"
        script += "driver.quit()\n"
        return script

    def _generate_import_statements(self):
        return (
            "import time\n"
            "from selenium import webdriver\n"
            "from selenium.webdriver.common.by import By\n"
            "from selenium.common.exceptions import WebDriverException\n"
            "from selenium.webdriver.support.ui import WebDriverWait\n"
            "from selenium.webdriver.support import expected_conditions as EC\n"
        )

    def _generate_actions(self, actions):
        action_script = ""
        for action in actions:
            action_script += self._generate_action(action)
        return action_script

    def _generate_action(self, action):
        wait = 5 #need to work out wait times
        action_type, xpath, value = action
        if action_type == "click":
            return (
                f"wait = WebDriverWait(driver, {wait})\n"
                f"element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                f"element.click()\n"
            )
        elif action_type == "type":
            return (
                f"wait = WebDriverWait(driver, {wait})\n"
                f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                f"element.send_keys('{value}')\n"
            )
        elif action_type == "input":
            return (
                f"wait = WebDriverWait(driver, {wait})\n"
                f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                f"element.clear()\n"
                f"element.send_keys('{value}')\n"
            )
        elif action_type == "submit":
            return (
                f"wait = WebDriverWait(driver, {wait})\n"
                f"element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                f"element.submit()\n"
            )

class SeleniumScriptGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selenium Script Generator")

        self.script_generator = ScriptGenerator()

        self._create_browser_selection()
        self._create_url_input()
        self._create_actions_input()
        self._create_generate_button()
        self._create_generated_script_output()

    def _create_browser_selection(self):
        browser_label = tk.Label(self.root, text="Select a Browser:")
        browser_label.pack()

        self.browser_var = tk.StringVar()
        self.browser_var.set(ScriptGenerator.DEFAULT_BROWSER)  # Default selection
        browser_option = ttk.Combobox(self.root, textvariable=self.browser_var, values=["Chrome", "Firefox"])
        browser_option.pack()

    def _create_url_input(self):
        url_label = tk.Label(self.root, text="URL:")
        url_label.pack()

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

    def _create_actions_input(self):
        actions_label = tk.Label(self.root, text="Actions (One per line in format 'action|XPath|Value'):")
        actions_label.pack()

        self.actions_text = tk.Text(self.root, height=10, width=50)
        self.actions_text.pack()

    def _create_generate_button(self):
        generate_button = tk.Button(self.root, text="Generate Script", command=self.generate_and_run_script)
        generate_button.pack()

    def _create_generated_script_output(self):
        self.generated_script = tk.Text(self.root, height=10, width=50)
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
            self.root.update_idletasks()
            try:
                exec(script)  # Run the generated script
                # self.root.quit() #exit the GUI
            except Exception as e:
                self.generated_script.delete("1.0", tk.END)
                self.generated_script.insert(tk.END, f"Error: {str(e)}")
        else:
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert(tk.END, "Please select a browser, enter a URL, and define actions.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeleniumScriptGeneratorApp(root)
    root.wm_attributes('-topmost', 1) #set to stay on top
    root.mainloop()
