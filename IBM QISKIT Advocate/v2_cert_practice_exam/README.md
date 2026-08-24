# Qiskit v2.x Certification Practice Exam Simulator

A comprehensive, interactive practice exam simulator designed to prepare candidates for the **IBM Certified Associate Developer - Quantum Computing v2** (C1000-179) certification. 

This tool was built to master the nuances of the Qiskit v2.x architecture and serves as a valuable resource for the quantum computing community and Qiskit Advocate Program candidates.

## ✨ Features

*   📚 **Extensive Question Database**: A robust JSON database containing **60 advanced questions** that strictly align with the official IBM syllabus. Topics include Instruction Set Architecture (ISA) transpilation, V2 Primitives (`SamplerV2`, `EstimatorV2`), `qiskit.quantum_info`, dynamic circuits, and OpenQASM 3.0.
*   🎲 **Randomized Testing**: To prevent memorization, the simulator randomly selects exactly **20 questions** from the database for each session, mimicking a real exam environment.
*   💻 **Interactive Browser UI**: A sleek, responsive HTML interface featuring a built-in timer, live scoring, and instant technical feedback for incorrect answers.
*   🌓 **Theme Toggle**: Easily switch between Dark and Light modes for comfortable, long-term studying.
*   📊 **ASCII Diagram Support**: Custom CSS rendering ensures that quantum circuit text diagrams and Python code blocks are displayed perfectly.
*   🔒 **Local Server Execution**: Uses a lightweight, native Python HTTP server to bypass browser CORS restrictions and open the exam smoothly in your default browser.
*   ⚡ **Automated Environment**: Uses `uv` and a bash script to instantly manage virtual environments and dependencies.

## 📂 Project Structure

*   `start_exam.sh`: The automated bash script that handles the `uv` virtual environment, installs dependencies, and launches the app.
*   `run_browser_exam.py`: The main Python execution script. It reads the database, generates the interactive HTML UI, and spins up a local server.
*   `qiskit_v2_database.json`: The core database containing all questions, options, correct answers, and detailed technical explanations. 
*   `requirements.txt`: The project dependencies (located in the root directory).

## 🚀 How to Use

The project includes an automated launcher that uses `uv` for blazing-fast virtual environment management.

### Method 1: Automated Launch (Recommended)
1. Ensure you have `uv` installed (`pip install uv`).
2. Make the script executable (only needed the first time):
   ```bash
   chmod +x start_exam.sh
   ```
3. Run the launcher:
   ```bash
   ./start_exam.sh
   ```
   *This will automatically create a `.venv`, install the required Qiskit packages, and launch the exam in your browser.*

### Method 2: Manual Launch
If you prefer not to use the bash script, the simulator itself has zero external dependencies and runs on the Python Standard Library:
```bash
python run_browser_exam.py
```

### Navigating the Exam
*   The script will spin up a local server and attempt to open Google Chrome automatically.
*   If your environment (like WSL or a headless setup) prevents the browser from opening, simply `Ctrl + Click` or copy/paste the local link provided in the terminal (usually `http://localhost:8000/practice_exam_ui.html`).
*   To stop the server once you are done studying, press `Ctrl + C` in your terminal.

## 📖 Syllabus Coverage

The questions in this simulator are proportionally distributed to match the real exam objectives:
*   Section 1: Perform quantum operations
*   Section 2: Visualize quantum circuits, measurements, and states
*   Section 3: Create quantum circuits
*   Section 4: Run quantum circuits
*   Section 5: Use the sampler primitive
*   Section 6: Use the estimator primitive
*   Section 7: Retrieve and analyze the results of quantum circuits
*   Section 8: Operate with OpenQASM

---
*Developed as part of the Qiskit Advocate Program journey.*