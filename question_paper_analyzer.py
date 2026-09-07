# ============================================================
# SMART QUESTION PAPER ANALYZER
# Advanced NLP Based GUI Application
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
from collections import Counter
from difflib import SequenceMatcher


# ============================================================
# NLP FUNCTIONS
# ============================================================

STOPWORDS = {
    "the", "is", "a", "an", "of", "to", "in", "and",
    "for", "on", "with", "what", "are", "how", "why",
    "when", "where", "which", "who", "this", "that",
    "these", "those", "from", "by", "be", "as", "at",
    "or", "it", "its", "into", "their", "than",
    "explain", "write", "define", "give", "describe",
    "discuss", "state", "list", "using"
}


def clean_text(text):
    """Convert text to lowercase and remove unwanted characters."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text):
    """Split text into words."""
    return text.split()


def remove_stopwords(words):
    """Remove common stopwords."""
    return [
        word for word in words
        if word not in STOPWORDS and len(word) > 2
    ]


def get_questions(text):
    """
    Extract questions from the question paper.
    Supports numbered questions and question-mark based text.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    questions = []

    # Numbered questions
    for line in lines:
        if re.match(r"^\s*(\d+[\.\)]|Q\.?\s*\d+)", line, re.IGNORECASE):
            questions.append(line)

    # If no numbered questions are found,
    # split using question marks.
    if not questions:
        parts = re.split(r"\?", text)

        for part in parts:
            part = part.strip()

            if part:
                questions.append(part + "?")

    return questions


def analyze_text(text):
    """Perform complete NLP analysis."""

    cleaned = clean_text(text)

    all_words = tokenize(cleaned)

    meaningful_words = remove_stopwords(all_words)

    frequency = Counter(meaningful_words)

    questions = get_questions(text)

    return (
        all_words,
        meaningful_words,
        frequency,
        questions
    )


def find_repeated_questions(questions):
    """
    Find similar/repeated questions using text similarity.
    """

    repeated = []

    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):

            q1 = clean_text(questions[i])
            q2 = clean_text(questions[j])

            similarity = SequenceMatcher(
                None,
                q1,
                q2
            ).ratio()

            if similarity >= 0.70:
                repeated.append(
                    (
                        questions[i],
                        questions[j],
                        round(similarity * 100, 1)
                    )
                )

    return repeated


# ============================================================
# GUI FUNCTIONS
# ============================================================

def upload_file():

    file_path = filedialog.askopenfilename(
        title="Select Question Paper",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if file_path:

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            input_text.delete(
                "1.0",
                tk.END
            )

            input_text.insert(
                tk.END,
                text
            )

            status_label.config(
                text="Question paper loaded successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "File Error",
                str(error)
            )


def analyze():

    text = input_text.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showwarning(
            "No Input",
            "Please enter or upload a question paper."
        )

        return

    (
        all_words,
        meaningful_words,
        frequency,
        questions
    ) = analyze_text(text)

    # --------------------------------------------------------
    # Dashboard statistics
    # --------------------------------------------------------

    total_words = len(all_words)

    unique_words = len(set(all_words))

    total_questions = len(questions)

    meaningful_count = len(meaningful_words)

    total_words_value.config(
        text=str(total_words)
    )

    unique_words_value.config(
        text=str(unique_words)
    )

    total_questions_value.config(
        text=str(total_questions)
    )

    keywords_value.config(
        text=str(len(frequency))
    )

    # --------------------------------------------------------
    # Keyword table
    # --------------------------------------------------------

    for item in keyword_table.get_children():

        keyword_table.delete(item)

    for word, count in frequency.most_common(15):

        keyword_table.insert(
            "",
            tk.END,
            values=(word, count)
        )

    # --------------------------------------------------------
    # Topic analysis
    # --------------------------------------------------------

    for item in topic_table.get_children():

        topic_table.delete(item)

    for word, count in frequency.most_common(10):

        topic_table.insert(
            "",
            tk.END,
            values=(
                word.capitalize(),
                count
            )
        )

    # --------------------------------------------------------
    # Question analysis
    # --------------------------------------------------------

    for item in question_table.get_children():

        question_table.delete(item)

    for number, question in enumerate(
        questions,
        start=1
    ):

        words_in_question = len(
            tokenize(clean_text(question))
        )

        question_table.insert(
            "",
            tk.END,
            values=(
                number,
                question,
                words_in_question
            )
        )

    # --------------------------------------------------------
    # Repeated questions
    # --------------------------------------------------------

    for item in repeated_table.get_children():

        repeated_table.delete(item)

    repeated_questions = find_repeated_questions(
        questions
    )

    if repeated_questions:

        for q1, q2, similarity in repeated_questions:

            repeated_table.insert(
                "",
                tk.END,
                values=(
                    q1,
                    q2,
                    f"{similarity}%"
                )
            )

    else:

        repeated_table.insert(
            "",
            tk.END,
            values=(
                "No repeated/similar questions found.",
                "-",
                "-"
            )
        )

    # --------------------------------------------------------
    # Analysis summary
    # --------------------------------------------------------

    summary_text.delete(
        "1.0",
        tk.END
    )

    summary_text.insert(
        tk.END,
        "SMART QUESTION PAPER ANALYSIS REPORT\n"
    )

    summary_text.insert(
        tk.END,
        "=" * 50 + "\n\n"
    )

    summary_text.insert(
        tk.END,
        f"Total Words       : {total_words}\n"
    )

    summary_text.insert(
        tk.END,
        f"Unique Words      : {unique_words}\n"
    )

    summary_text.insert(
        tk.END,
        f"Total Questions   : {total_questions}\n"
    )

    summary_text.insert(
        tk.END,
        f"Meaningful Words  : {meaningful_count}\n"
    )

    summary_text.insert(
        tk.END,
        f"Unique Keywords   : {len(frequency)}\n\n"
    )

    summary_text.insert(
        tk.END,
        "Top Keywords:\n"
    )

    summary_text.insert(
        tk.END,
        "-" * 30 + "\n"
    )

    for word, count in frequency.most_common(10):

        summary_text.insert(
            tk.END,
            f"{word:<20} {count}\n"
        )

    summary_text.insert(
        tk.END,
        "\nNLP Processing Applied:\n"
    )

    summary_text.insert(
        tk.END,
        "• Text Cleaning\n"
        "• Tokenization\n"
        "• Stop-word Removal\n"
        "• Keyword Extraction\n"
        "• Frequency Analysis\n"
        "• Question Similarity Analysis\n"
        "• Topic Frequency Analysis\n"
    )

    status_label.config(
        text="Analysis completed successfully."
    )

    notebook.select(
        dashboard_tab
    )


def clear_all():

    input_text.delete(
        "1.0",
        tk.END
    )

    summary_text.delete(
        "1.0",
        tk.END
    )

    total_words_value.config(
        text="0"
    )

    unique_words_value.config(
        text="0"
    )

    total_questions_value.config(
        text="0"
    )

    keywords_value.config(
        text="0"
    )

    for table in [
        keyword_table,
        topic_table,
        question_table,
        repeated_table
    ]:

        for item in table.get_children():

            table.delete(item)

    
        status_label.config(
        text="Ready for new analysis."
    )


def save_report():

    if not keyword_table.get_children():

        messagebox.showwarning(
            "No Analysis",
            "Please analyze the question paper first."
        )

        return

    file_path = filedialog.asksaveasfilename(
        title="Save Analysis Report",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt")
        ]
    )

    if not file_path:

        return

    try:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                summary_text.get(
                    "1.0",
                    tk.END
                )
            )

            file.write(
                "\n\nTOP KEYWORDS\n"
            )

            file.write(
                "=" * 40 + "\n"
            )

            for item in keyword_table.get_children():

                values = keyword_table.item(
                    item
                )["values"]

                file.write(
                    f"{values[0]} : {values[1]}\n"
                )

            file.write(
                "\n\nQUESTION ANALYSIS\n"
            )

            file.write(
                "=" * 40 + "\n"
            )

            for item in question_table.get_children():

                values = question_table.item(
                    item
                )["values"]

                file.write(
                    f"{values[0]}. {values[1]}\n"
                )

            file.write(
                "\n\nSIMILAR / REPEATED QUESTIONS\n"
            )

            file.write(
                "=" * 40 + "\n"
            )

            for item in repeated_table.get_children():

                values = repeated_table.item(
                    item
                )["values"]

                file.write(
                    f"{values[0]}  <-->  "
                    f"{values[1]}  "
                    f"Similarity: {values[2]}\n"
                )

        messagebox.showinfo(
            "Success",
            "Analysis report saved successfully!"
        )

        status_label.config(
            text="Report saved successfully."
        )

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            str(error)
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Smart Question Paper Analyzer"
)

root.geometry(
    "1100x750"
)

root.minsize(
    950,
    650
)

root.configure(
    bg="#EAF1F8"
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="SMART QUESTION PAPER ANALYZER",
    font=("Arial", 25, "bold"),
    bg="#EAF1F8",
    fg="#17365D"
)

title.pack(
    pady=(18, 3)
)


subtitle = tk.Label(
    root,
    text="Advanced NLP Based Question Paper Analysis System",
    font=("Arial", 12),
    bg="#EAF1F8",
    fg="#555555"
)

subtitle.pack(
    pady=(0, 12)
)


# ============================================================
# NOTEBOOK / TABS
# ============================================================

style = ttk.Style()

style.theme_use(
    "clam"
)

style.configure(
    "TNotebook",
    background="#EAF1F8"
)

style.configure(
    "TNotebook.Tab",
    font=("Arial", 10, "bold"),
    padding=[18, 8],
    background="#D9EAF7",
    foreground="#17365D"
)

style.map(
    "TNotebook.Tab",
    background=[("selected", "#5B9BD5")],
    foreground=[("selected", "white")]
)


notebook = ttk.Notebook(
    root
)

notebook.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=5
)


# ============================================================
# INPUT TAB
# ============================================================

input_tab = tk.Frame(
    notebook,
    bg="white"
)

notebook.add(
    input_tab,
    text="  Input  "
)


input_heading = tk.Label(
    input_tab,
    text="Enter or Upload Question Paper",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="#17365D"
)

input_heading.pack(
    pady=(20, 10)
)


input_text = tk.Text(
    input_tab,
    font=("Arial", 11),
    wrap="word",
    relief="solid",
    borderwidth=2,
    bg="#F0F8FF",
    fg="#17365D",
    insertbackground="#17365D",
    selectbackground="#5B9BD5",
    selectforeground="white"
)

input_text.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    input_tab,
    bg="white"
)

button_frame.pack(
    pady=15
)


upload_button = tk.Button(
    button_frame,
    text="📂 Upload",
    command=upload_file,
    font=("Arial", 10, "bold"),
    bg="#3498DB",
    fg="white",
    activebackground="#217DBB",
    activeforeground="white",
    relief="flat",
    padx=22,
    pady=10,
    cursor="hand2"
)

upload_button.grid(
    row=0,
    column=0,
    padx=6
)


analyze_button = tk.Button(
    button_frame,
    text="🔍 Analyze",
    command=analyze,
    font=("Arial", 10, "bold"),
    bg="#27AE60",
    fg="white",
    activebackground="#1E8449",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

analyze_button.grid(
    row=0,
    column=1,
    padx=6
)


clear_button = tk.Button(
    button_frame,
    text="🗑 Clear",
    command=clear_all,
    font=("Arial", 10, "bold"),
    bg="#E67E22",
    fg="white",
    activebackground="#CA6F1E",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=2,
    padx=6
)


save_button = tk.Button(
    button_frame,
    text="💾 Save Report",
    command=save_report,
    font=("Arial", 10, "bold"),
    bg="#8E44AD",
    fg="white",
    activebackground="#71368A",
    activeforeground="white",
    relief="flat",
    padx=22,
    pady=10,
    cursor="hand2"
)

save_button.grid(
    row=0,
    column=3,
    padx=6
)


# ============================================================
# DASHBOARD TAB
# ============================================================

dashboard_tab = tk.Frame(
    notebook,
    bg="#EAF1F8"
)

notebook.add(
    dashboard_tab,
    text="  Dashboard  "
)


dashboard_title = tk.Label(
    dashboard_tab,
    text="Analysis Dashboard",
    font=("Arial", 18, "bold"),
    bg="#EAF1F8",
    fg="#17365D"
)

dashboard_title.pack(
    pady=20
)


stats_frame = tk.Frame(
    dashboard_tab,
    bg="#EAF1F8"
)

stats_frame.pack(
    pady=10
)


def create_stat_card(
    parent,
    title_text,
    number
):

    card = tk.Frame(
        parent,
        bg="white",
        relief="solid",
        borderwidth=1,
        width=190,
        height=110
    )

    card.pack_propagate(
        False
    )

    title_label = tk.Label(
        card,
        text=title_text,
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#555555"
    )

    title_label.pack(
        pady=(15, 3)
    )

    value_label = tk.Label(
        card,
        text=number,
        font=("Arial", 24, "bold"),
        bg="white",
        fg="#17365D"
    )

    value_label.pack()

    return card, value_label


card1, total_words_value = create_stat_card(
    stats_frame,
    "TOTAL WORDS",
    "0"
)

card1.grid(
    row=0,
    column=0,
    padx=10
)


card2, unique_words_value = create_stat_card(
    stats_frame,
    "UNIQUE WORDS",
    "0"
)

card2.grid(
    row=0,
    column=1,
    padx=10
)


card3, total_questions_value = create_stat_card(
    stats_frame,
    "QUESTIONS",
    "0"
)

card3.grid(
    row=0,
    column=2,
    padx=10
)


card4, keywords_value = create_stat_card(
    stats_frame,
    "KEYWORDS",
    "0"
)

card4.grid(
    row=0,
    column=3,
    padx=10
)


# ============================================================
# KEYWORD TAB
# ============================================================

keyword_tab = tk.Frame(
    notebook,
    bg="white"
)

notebook.add(
    keyword_tab,
    text="  Keywords  "
)


keyword_heading = tk.Label(
    keyword_tab,
    text="Top Keywords and Frequency",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#17365D"
)

keyword_heading.pack(
    pady=20
)


keyword_table = ttk.Treeview(
    keyword_tab,
    columns=("Keyword", "Frequency"),
    show="headings"
)

keyword_table.heading(
    "Keyword",
    text="Keyword"
)

keyword_table.heading(
    "Frequency",
    text="Frequency"
)

keyword_table.column(
    "Keyword",
    width=450,
    anchor="center"
)

keyword_table.column(
    "Frequency",
    width=250,
    anchor="center"
)

keyword_table.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=10
)


# ============================================================
# TOPICS TAB
# ============================================================

topic_tab = tk.Frame(
    notebook,
    bg="white"
)

notebook.add(
    topic_tab,
    text="  Topics  "
)


topic_heading = tk.Label(
    topic_tab,
    text="Frequently Appearing Topics / Keywords",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#17365D"
)

topic_heading.pack(
    pady=20
)


topic_table = ttk.Treeview(
    topic_tab,
    columns=("Topic", "Frequency"),
    show="headings"
)

topic_table.heading(
    "Topic",
    text="Topic / Keyword"
)

topic_table.heading(
    "Frequency",
    text="Frequency"
)

topic_table.column(
    "Topic",
    width=450,
    anchor="center"
)

topic_table.column(
    "Frequency",
    width=250,
    anchor="center"
)

topic_table.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=10
)


# ============================================================
# QUESTIONS TAB
# ============================================================

question_tab = tk.Frame(
    notebook,
    bg="white"
)

notebook.add(
    question_tab,
    text="  Questions  "
)


question_heading = tk.Label(
    question_tab,
    text="Question-wise Analysis",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#17365D"
)

question_heading.pack(
    pady=15
)


question_table = ttk.Treeview(
    question_tab,
    columns=(
        "Number",
        "Question",
        "Words"
    ),
    show="headings"
)


question_table.heading(
    "Number",
    text="No."
)

question_table.heading(
    "Question",
    text="Question"
)

question_table.heading(
    "Words",
    text="Words"
)


question_table.column(
    "Number",
    width=70,
    anchor="center"
)

question_table.column(
    "Question",
    width=700,
    anchor="w"
)

question_table.column(
    "Words",
    width=100,
    anchor="center"
)


question_table.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


# ============================================================
# REPEATED QUESTIONS TAB
# ============================================================

repeated_tab = tk.Frame(
    notebook,
    bg="white"
)

notebook.add(
    repeated_tab,
    text="  Similar Questions  "
)


repeated_heading = tk.Label(
    repeated_tab,
    text="Repeated / Similar Questions",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#17365D"
)

repeated_heading.pack(
    pady=15
)


repeated_table = ttk.Treeview(
    repeated_tab,
    columns=(
        "Question 1",
        "Question 2",
        "Similarity"
    ),
    show="headings"
)


repeated_table.heading(
    "Question 1",
    text="Question 1"
)

repeated_table.heading(
    "Question 2",
    text="Question 2"
)

repeated_table.heading(
    "Similarity",
    text="Similarity"
)


repeated_table.column(
    "Question 1",
    width=350,
    anchor="w"
)

repeated_table.column(
    "Question 2",
    width=350,
    anchor="w"
)

repeated_table.column(
    "Similarity",
    width=120,
    anchor="center"
)


repeated_table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# ============================================================
# REPORT TAB
# ============================================================

report_tab = tk.Frame(
    notebook,
    bg="white"
)

notebook.add(
    report_tab,
    text="  Report  "
)


report_heading = tk.Label(
    report_tab,
    text="Analysis Report",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#17365D"
)

report_heading.pack(
    pady=15
)


summary_text = tk.Text(
    report_tab,
    font=("Consolas", 11),
    wrap="word",
    relief="solid",
    borderwidth=1
)

summary_text.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# ============================================================
# STATUS BAR
# ============================================================

status_label = tk.Label(
    root,
    text="Ready for question paper analysis.",
    font=("Arial", 9),
    bg="#D9EAF7",
    fg="#17365D",
    anchor="w",
    padx=10
)

status_label.pack(
    fill="x",
    side="bottom"
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()