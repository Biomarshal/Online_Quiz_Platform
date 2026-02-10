import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QRadioButton, QButtonGroup,
    QMessageBox, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt


# ================= QUIZ DATA =================
QUIZ = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": 2
    },
    {
        "question": "Which language is most used in AI?",
        "options": ["Python", "C++", "Java", "HTML"],
        "answer": 0
    },
    {
        "question": "2 + 2 × 2 = ?",
        "options": ["6", "8", "4", "10"],
        "answer": 0
    },
    {
        "question": "Who developed relativity?",
        "options": ["Newton", "Einstein", "Tesla", "Edison"],
        "answer": 1
    }
]


# ================= MAIN APP =================
class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Online Quiz")
        self.resize(520, 420)

        self.q_index = 0
        self.score = 0

        # Progress
        self.progress = QProgressBar()
        self.progress.setFixedHeight(12)
        self.progress.setTextVisible(False)

        # Question Card
        self.card = QFrame()
        self.card.setObjectName("card")

        self.question = QLabel()
        self.question.setWordWrap(True)
        self.question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question.setObjectName("question")

        # Options
        self.group = QButtonGroup(self)
        self.opts_layout = QVBoxLayout()

        # Next button
        self.next_btn = QPushButton("Next Question")
        self.next_btn.clicked.connect(self.next_question)

        # Layouts
        card_layout = QVBoxLayout(self.card)
        card_layout.addWidget(self.question)
        card_layout.addLayout(self.opts_layout)

        main = QVBoxLayout(self)
        main.setContentsMargins(40, 30, 40, 30)
        main.setSpacing(20)

        main.addWidget(self.progress)
        main.addWidget(self.card)
        main.addWidget(self.next_btn)

        self.set_dark_theme()
        self.load_question()

    # ================= THEME =================
    def set_dark_theme(self):
        self.setStyleSheet("""
        QWidget {
            background:#0f172a;
            color:white;
            font-family:Segoe UI;
        }

        QFrame#card {
            background:#1e293b;
            border-radius:16px;
            padding:20px;
        }

        QLabel#question {
            font-size:20px;
            font-weight:600;
            margin-bottom:15px;
        }

        QRadioButton {
            background:#334155;
            padding:12px;
            border-radius:10px;
            font-size:15px;
        }

        QRadioButton::indicator {
            width:0px;
        }

        QRadioButton:hover {
            background:#475569;
        }

        QRadioButton:checked {
            background:#22c55e;
            color:black;
            font-weight:bold;
        }

        QPushButton {
            background:#38bdf8;
            color:black;
            padding:14px;
            border-radius:12px;
            font-size:16px;
            font-weight:bold;
        }

        QPushButton:hover {
            background:#0ea5e9;
        }

        QProgressBar {
            background:#1f2937;
            border-radius:6px;
        }

        QProgressBar::chunk {
            background:#22c55e;
            border-radius:6px;
        }
        """)

    # ================= LOAD QUESTION =================
    def load_question(self):
        self.clear_options()

        q = QUIZ[self.q_index]

        self.question.setText(
            f"Question {self.q_index+1} of {len(QUIZ)}\n\n{q['question']}"
        )

        self.progress.setValue(
            int((self.q_index/len(QUIZ))*100)
        )

        for i, opt in enumerate(q["options"]):
            rb = QRadioButton(opt)
            self.group.addButton(rb, i)
            self.opts_layout.addWidget(rb)

    def clear_options(self):
        for i in reversed(range(self.opts_layout.count())):
            w = self.opts_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

    # ================= NEXT =================
    def next_question(self):
        sel = self.group.checkedId()

        if sel == -1:
            QMessageBox.warning(self, "Select", "Choose an answer")
            return

        if sel == QUIZ[self.q_index]["answer"]:
            self.score += 1

        self.q_index += 1

        if self.q_index >= len(QUIZ):
            self.finish()
        else:
            self.load_question()

    # ================= RESULT =================
    def finish(self):
        percent = int((self.score/len(QUIZ))*100)

        msg = QMessageBox(self)
        msg.setWindowTitle("Quiz Completed")
        msg.setText(
            f"Score: {self.score}/{len(QUIZ)}\n"
            f"Percentage: {percent}%"
        )

        r = msg.addButton("Restart", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        if msg.clickedButton() == r:
            self.q_index = 0
            self.score = 0
            self.load_question()


# ================= RUN =================
app = QApplication(sys.argv)
w = QuizApp()
w.show()
sys.exit(app.exec())
