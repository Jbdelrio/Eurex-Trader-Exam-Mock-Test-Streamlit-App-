# 📘 Eurex Trader Exam – Mock Test (Streamlit App)

This project is a full-featured **mock exam simulator** for the official **Eurex Trader Examination**, built using **Streamlit**.
It replicates the real structure, scoring rules, and timing conditions used in the actual exam.

Designed for fast, accurate, and repeated training before taking the certification.

---

## 📄 Official Source

All questions used in this mock exam are derived from the official document:

**“Eurex® trader exam – Questions and Answers (Valid from 03.03.2025)”**,
*December 2024 Edition* 

This repository is strictly for educational and exam preparation purposes.

## 🚀 Features

### ✅ **Realistic Question Selection (Based on Eurex Exam Structure)**

The mock exam automatically selects:

#### **Rules & Regulations (Questions 1–45)**

* **5** True/False
* **4** Multiple Choice
* **6** Single Choice

#### **Functionality of Trading (Questions 46–105)**

* **4** True/False
* **8** Multiple Choice
* **8** Single Choice

A total of **35 questions**, exactly like the real exam.

---

## ⏱️ **20-Minute Exam Timer**

A visible countdown timer (mm:ss) starts as soon as the test begins.
When the timer reaches zero, the test is automatically submitted.

---

## 🧠 Scoring System (Official Eurex Rules)

### **True/False (TF)**

* One correct answer
* ✔️ Correct = **+2 points**
* ❌ Wrong = **0 points**

### **Single Choice (SC)**

* One correct answer
* ✔️ Correct = **+2 points**
* ❌ Wrong = **0 points**

### **Multiple Choice (MC)**

Several correct answers possible (up to four).
Scoring is strictly based on Eurex’ rules:

#### ⭐ FULL SCORE MODE

* ✔️ **+4 points** if *all* correct answers are selected and *no* incorrect answers are selected.

#### 📊 PARTIAL SCORING MODE

If not perfect:

* **+1** for each correct selected
* **+1** for each incorrect *not* selected
* **−1** for each incorrect selected
* **−1** for each correct *not* selected
* Final score is **min = 0**, **max = 4**

---

## 📊 Feedback After Submission

After submitting:

* Each question shows:

  * 🟢 **Correct** or 🔴 **Incorrect**
  * The **correct answer(s)** clearly displayed
* Final score is computed and displayed

---

## 🔁 Multiple Test Runs

Each time you click **“Take Another Test”**, a brand new set of questions is drawn from the pool.

Perfect for intensive training.

---

## 📂 Project Structure

```
📁 eurex-mock-exam
│── app.py                     # Main Streamlit application
│── eurex_questions_auto.csv   # All parsed questions (IDs 1–105)
│── README.md                  # Documentation
│── requirements.txt           # Python dependencies
```

---

## ▶️ How to Run Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Launch the app

```bash
streamlit run app.py
```

Your browser will open automatically at:

```
http://localhost:8501
```

---

## 📦 Requirements

Create a `requirements.txt` like this:

```
streamlit
pandas
```

(If OCR or PDF processing is required in future versions, add libraries like `pytesseract`, `pdf2image`, etc.)

---

## 📝 CSV Format (Question Bank)

The app uses a CSV with the following structure:

```
id,question,is_multiple,option_a,option_b,option_c,option_d,correct
```

* `is_multiple = TRUE` → MC
* `is_multiple = FALSE` + answers include “True”/“False” → TF
* Otherwise → SC
* `correct` contains letters separated by `;` (e.g., `"A;C;D"`)

---

## 🎯 Purpose

This project provides a **high-quality training environment** for candidates preparing for the **Eurex Trader Exam**, replicating:

* Question types
* Topic distribution
* Time constraint
* Scoring mechanics
* Answer review

It's ideal for traders, students, and analysts working in **derivatives trading**, **market operations**, or **risk management**.

---

## 🙌 Contributions

Pull requests are welcome.
Feel free to open issues to request improvements or report bugs.

---

 
