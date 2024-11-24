# prompt: Convert the above code to be run on desktop. UI should look modern.

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import webbrowser

def generate_mathjax_html(question_numbers, answers):
    # Ensure the lengths match
    if len(question_numbers) != len(answers):
        raise ValueError("The number of question IDs must match the number of answers.")

    # HTML content with placeholders
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PDF Viewer with Collapsible Answers</title>

  <!-- MathJax -->
  <script type="text/javascript" async 
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
  </script>

  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; height: 100vh; display: flex; flex-direction: column; }}
    .navbar {{ position: fixed; top: 0; width: 100%; z-index: 1000; background-color: #333; display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); }}
    .navbar a {{ color: white; text-decoration: none; margin: 0 10px; font-size: 16px; padding: 5px 10px; border-radius: 5px; transition: background-color 0.3s ease; }}
    .navbar a:hover {{ background-color: #575757; }}
    .navbar .logo {{ font-weight: bold; font-size: 20px; color: white; }}
    .container {{ display: flex; flex: 1; margin-top: 60px; height: calc(100vh - 60px); overflow: hidden; }}
    .pdf-container {{ width: 70%; position: relative; overflow: auto; background-color: #f4f4f4; }}
    .pdf-frame {{ width: 100%; height: 100%; border: none; }}
    .answer-sidebar {{ width: 30%; background-color: #222; color: white; border-left: 1px solid #444; padding: 10px; overflow-y: auto; }}
    .buttons button {{ width: 48%; margin-bottom: 10px; padding: 10px; color: white; border: none; border-radius: 5px; cursor: pointer; text-align: left; }}
    .show-all-answers {{ background-color: #28a745; }}
    .show-all-answers:hover {{ background-color: #218838; }}
    .collapse-all {{ background-color: #dc3545; }}
    .collapse-all:hover {{ background-color: #c82333; }}
    .collapsible {{ background-color: #333; color: white; cursor: pointer; padding: 15px; text-align: left; border: none; outline: none; font-size: 16px; border-radius: 5px; margin-bottom: 10px; }}
    .collapsible:hover {{ background-color: #444; }}
    .content {{ padding: 0 15px; max-height: 0; overflow: hidden; transition: max-height 0.2s ease-out; background-color: #444; border-radius: 5px; margin-bottom: 15px; }}
    .content p {{ font-size: 14px; color: #ddd; margin: 10px 0; }}
  </style>
</head>
<body>

  <div class="navbar">
    <div class="logo">My Project</div>
    <div class="links">
      <a href="#">Home</a>
      <a href="#">Solved Papers</a>
      <a href="#">View Notes</a>
    </div>
  </div>

  <div class="container">
    <div class="pdf-container">
      <iframe class="pdf-frame" src="example.pdf"></iframe>
    </div>

    <div class="answer-sidebar">
      <div class="buttons">
        <button class="show-all-answers" onclick="showAllAnswers()">Show All Answers</button>
        <button class="collapse-all" onclick="collapseAll()">Collapse All Answers</button>
      </div>
      <div id="answerSection">
        {generate_answer_sections(question_numbers, answers)}
      </div>
    </div>
  </div>

<script>
  function showAllAnswers() {{
    const contents = document.querySelectorAll(".content");
    contents.forEach(content => {{
      content.style.maxHeight = content.scrollHeight + "px";
    }});

    const collapsibles = document.querySelectorAll(".collapsible");
    collapsibles.forEach(collapsible => {{
      collapsible.classList.add("active");
    }});
  }}

  function collapseAll() {{
    const contents = document.querySelectorAll(".content");
    contents.forEach(content => {{
      content.style.maxHeight = null;
    }});

    const collapsibles = document.querySelectorAll(".collapsible");
    collapsibles.forEach(collapsible => {{
      collapsible.classList.remove("active");
    }});
  }}

  document.querySelectorAll(".collapsible").forEach(button => {{
    button.addEventListener("click", () => {{
      button.classList.toggle("active");
      const content = button.nextElementSibling;
      if (content.style.maxHeight) {{
        content.style.maxHeight = null;
      }} else {{
        content.style.maxHeight = content.scrollHeight + "px";
      }}
    }});
  }});
</script>

</body>
</html>
"""



    # Write to an HTML file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML file generated: output.html")

def generate_answer_sections(question_numbers, answers):
    sections = ""
    for q_id, answer in zip(question_numbers, answers):
        sections += f"""
        <button class="collapsible">Answer {q_id}</button>
        <div class="content">
          <p>{answer}</p>
        </div>
        """
    return sections


def add_question():
    q_no = question_entry.get()
    solution = answer_text.get("1.0", tk.END)
    if q_no and solution:
        question_numbers.append(q_no)
        answers.append(solution)
        question_entry.delete(0, tk.END)
        answer_text.delete("1.0", tk.END)
        update_list()


def create_html():
    if question_numbers and answers:
        generate_mathjax_html(question_numbers, answers)
        webbrowser.open("output.html")  # Open in default browser
    else:
        status_label.config(text="Please add questions and answers first.")


def update_list():
    question_listbox.delete(0, tk.END)
    for i, (q, a) in enumerate(zip(question_numbers, answers)):
        question_listbox.insert(tk.END, f"Question {i+1}: {q}")


# Initialize data structures
question_numbers = []
answers = []


# Create main window
window = tk.Tk()
window.title("Interactive Question & Answer Tool")
window.geometry("800x600")  # Adjust window size
window.configure(bg="#f0f0f0") # Modern background

# Styling
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#4CAF50") #Green color, flat button
style.map("TButton", background=[("active", "#45a049")]) #Darker green on click

# Create and place widgets
question_label = ttk.Label(window, text="Question Number:")
question_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

question_entry = ttk.Entry(window, width=20)  # Adjusted width
question_entry.grid(row=0, column=1, padx=10, pady=10)

answer_label = ttk.Label(window, text="Answer:")
answer_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")

answer_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=10)  # Larger text area
answer_text.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10))


add_button = ttk.Button(window, text="Add Question", command=add_question)
add_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

create_button = ttk.Button(window, text="Create HTML", command=create_html)
create_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))

question_listbox = tk.Listbox(window, width=40, height=10)
question_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10))

status_label = ttk.Label(window, text="")
status_label.grid(row=6, column=0, columnspan=2, pady=5)

window.mainloop()


