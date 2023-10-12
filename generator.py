import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def output_script(script):
    with open("script.py", "w") as script_file:
        script_file.write(script)

def generate_script():
    selected_browser = browser_var.get()
    if selected_browser == "Chrome":
        driver = webdriver.Chrome()
    elif selected_browser == "Firefox":
        driver = webdriver.Firefox()
    else:
        generated_script.delete("1.0", tk.END)
        generated_script.insert(tk.END, "Please select a browser.")
        return

    script = ""
    script += "from selenium import webdriver\n"
    script += "from selenium.webdriver.common.by import By\n"
    script += "from selenium.webdriver.support.ui import WebDriverWait\n"
    script += "from selenium.webdriver.support import expected_conditions as EC\n"
    script += f"driver = webdriver.{selected_browser}()\n"

    url = url_entry.get()
    script += f"driver.get('{url}')\n"

    actions = actions_text.get("1.0", tk.END).strip().split("\n")
    for action in actions:
        parts = action.split("|")
        action_type = parts[0].strip()
        xpath = parts[1].strip()
        value = parts[2].strip() if len(parts) > 2 else None

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

    generated_script.delete("1.0", tk.END)
    generated_script.insert(tk.END, script)

    output_script(script)

root = tk.Tk()
root.title("Selenium Script Generator")

# Browser selection dropdown
browser_var = tk.StringVar()
browser_var.set("Chrome")  # Default selection
browser_label = tk.Label(root, text="Select a Browser:")
browser_label.pack()
browser_option = ttk.Combobox(root, textvariable=browser_var, values=["Chrome", "Firefox"])
browser_option.pack()

url_label = tk.Label(root, text="URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

actions_label = tk.Label(root, text="Actions (One per line in format 'action|XPath|Value'):")
actions_label.pack()

actions_text = tk.Text(root, height=10, width=50)
actions_text.pack()

generate_button = tk.Button(root, text="Generate Script", command=generate_script)
generate_button.pack()

generated_script = tk.Text(root, height=10, width=50)
generated_script.pack()

root.mainloop()
