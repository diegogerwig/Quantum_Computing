import os
import http.server
import socketserver

def create_and_serve_html_exam(db_path="qiskit_v2_database.json", html_filename="practice_exam_ui.html", port=8000):
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            questions_json = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{db_path}'. Ensure it is in the same directory.")
        return

    html_content = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qiskit v2.x Certification Exam</title>
    <style>
        :root {{
            --bg: #121212; --container-bg: #1e1e1e; --text: #e0e0e0; --accent: #4589ff; --border: #333; 
            --btn-bg: #2a2a2a; --btn-hover: #3a3a3a; --correct-bg: #193b2d; --correct-border: #24a148; 
            --correct-text: #6fdc8c; --incorrect-bg: #441418; --incorrect-border: #da1e28; 
            --incorrect-text: #ff8389; --feedback-bg: #1a2639; --code-bg: #2a2a2a;
        }}
        [data-theme="light"] {{
            --bg: #f4f7f6; --container-bg: #ffffff; --text: #333333; --accent: #0f62fe; --border: #e0e0e0; 
            --btn-bg: #f4f7f6; --btn-hover: #e5eaea; --correct-bg: #defbe6; --correct-border: #24a148; 
            --correct-text: #198038; --incorrect-bg: #fff1f1; --incorrect-border: #da1e28; 
            --incorrect-text: #a2191f; --feedback-bg: #e5f6ff; --code-bg: #f8f9fa;
        }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; transition: background 0.3s, color 0.3s; }}
        .exam-container {{ background: var(--container-bg); padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 100%; max-width: 800px; margin: 20px; transition: background 0.3s; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--accent); padding-bottom: 15px; margin-bottom: 20px; }}
        .header div {{ font-size: 1.1em; font-weight: bold; }}
        .stats {{ display: flex; gap: 20px; align-items: center; }}
        .stat-correct {{ color: #24a148; }}
        .stat-incorrect {{ color: #da1e28; }}
        #theme-toggle {{ background: none; border: 1px solid var(--border); border-radius: 4px; color: var(--text); padding: 5px 10px; cursor: pointer; transition: 0.3s; }}
        #theme-toggle:hover {{ background: var(--btn-hover); }}
        .question-title {{ font-size: 1.2em; color: var(--accent); margin-bottom: 10px; }}
        .question-text {{ font-size: 1.1em; margin-bottom: 25px; line-height: 1.5; white-space: pre-wrap; font-family: 'Consolas', 'Courier New', monospace; background-color: var(--code-bg); padding: 15px; border-radius: 5px; border: 1px solid var(--border); }}
        .options {{ display: flex; flex-direction: column; gap: 10px; }}
        .option-btn {{ background-color: var(--btn-bg); color: var(--text); border: 2px solid var(--border); padding: 15px; border-radius: 6px; font-size: 1em; cursor: pointer; text-align: left; transition: all 0.2s; font-family: 'Consolas', 'Courier New', monospace; white-space: pre-wrap; }}
        .option-btn:hover:not(:disabled) {{ background-color: var(--btn-hover); border-color: var(--accent); }}
        .option-btn:disabled {{ cursor: not-allowed; opacity: 0.8; }}
        .correct {{ background-color: var(--correct-bg) !important; border-color: var(--correct-border) !important; color: var(--correct-text) !important; }}
        .incorrect {{ background-color: var(--incorrect-bg) !important; border-color: var(--incorrect-border) !important; color: var(--incorrect-text) !important; }}
        .feedback {{ margin-top: 20px; padding: 15px; border-radius: 6px; background-color: var(--feedback-bg); border-left: 5px solid var(--accent); display: none; }}
        .next-btn {{ margin-top: 25px; background-color: var(--accent); color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1em; cursor: pointer; float: right; display: none; }}
        .next-btn:hover {{ opacity: 0.9; }}
        .result-screen {{ display: none; text-align: center; }}
        .result-screen h1 {{ color: var(--accent); }}
        .clear {{ clear: both; }}
    </style>
</head>
<body>
<div class="exam-container" id="exam-ui">
    <div class="header">
        <div id="progress-text">Question 1 / 20</div>
        <div class="stats">
            <div>Time: <span id="timer">00:00</span></div>
            <div class="stat-correct">Correct: <span id="score-correct">0</span></div>
            <div class="stat-incorrect">Incorrect: <span id="score-incorrect">0</span></div>
            <button id="theme-toggle" onclick="toggleTheme()">☀️ Light</button>
        </div>
    </div>
    <div class="question-title" id="q-topic">Topic</div>
    <div class="question-text" id="q-text">Question text goes here?</div>
    <div class="options" id="options-container"></div>
    <div class="feedback" id="feedback-box"><strong>Explanation:</strong> <span id="explanation-text"></span></div>
    <button class="next-btn" id="next-btn" onclick="loadNextQuestion()">Next Question</button>
    <div class="clear"></div>
</div>
<div class="exam-container result-screen" id="result-screen">
    <h1>Exam Completed!</h1>
    <h2 id="final-score"></h2>
    <h3 id="final-time"></h3>
    <p id="final-message" style="font-size: 1.2em; margin-top: 20px;"></p>
    <button class="next-btn" style="float:none; display:inline-block;" onclick="location.reload()">Retake Exam</button>
</div>
<script>
    const db = {questions_json};
    const TOTAL_QUESTIONS = 20; // Exact constraint
    let examQuestions = [];
    let currentIdx = 0;
    let correctAnswers = 0;
    let incorrectAnswers = 0;
    let startTime;
    let timerInterval;

    function toggleTheme() {{
        const root = document.documentElement;
        const btn = document.getElementById('theme-toggle');
        if (root.getAttribute('data-theme') === 'dark') {{
            root.setAttribute('data-theme', 'light');
            btn.innerText = '🌙 Dark';
        }} else {{
            root.setAttribute('data-theme', 'dark');
            btn.innerText = '☀️ Light';
        }}
    }}

    function shuffle(array) {{
        for (let i = array.length - 1; i > 0; i--) {{
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }}
        return array;
    }}

    function startExam() {{
        examQuestions = shuffle([...db]).slice(0, TOTAL_QUESTIONS);
        startTime = Date.now();
        timerInterval = setInterval(updateTimer, 1000);
        renderQuestion();
    }}

    function updateTimer() {{
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const s = String(elapsed % 60).padStart(2, '0');
        document.getElementById('timer').innerText = m + ':' + s;
    }}

    function renderQuestion() {{
        const q = examQuestions[currentIdx];
        document.getElementById('progress-text').innerText = `Question ${{currentIdx + 1}} / ${{TOTAL_QUESTIONS}}`;
        document.getElementById('q-topic').innerText = q.topic;
        document.getElementById('q-text').innerText = q.q;
        
        const optsContainer = document.getElementById('options-container');
        optsContainer.innerHTML = '';
        
        q.options.forEach(opt => {{
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.innerText = opt;
            const letter = opt.substring(0, 1);
            btn.onclick = () => checkAnswer(letter, btn, q);
            optsContainer.appendChild(btn);
        }});
        document.getElementById('feedback-box').style.display = 'none';
        document.getElementById('next-btn').style.display = 'none';
    }}

    function checkAnswer(selectedLetter, btnElement, qObj) {{
        const buttons = document.querySelectorAll('.option-btn');
        buttons.forEach(b => b.disabled = true);
        if (selectedLetter === qObj.ans) {{
            btnElement.classList.add('correct');
            correctAnswers++;
            document.getElementById('score-correct').innerText = correctAnswers;
        }} else {{
            btnElement.classList.add('incorrect');
            incorrectAnswers++;
            document.getElementById('score-incorrect').innerText = incorrectAnswers;
            buttons.forEach(b => {{
                if(b.innerText.startsWith(qObj.ans)) b.classList.add('correct');
            }});
        }}
        document.getElementById('explanation-text').innerText = qObj.exp;
        document.getElementById('feedback-box').style.display = 'block';
        
        const nextBtn = document.getElementById('next-btn');
        nextBtn.innerText = (currentIdx === TOTAL_QUESTIONS - 1) ? 'Finish Exam' : 'Next Question';
        nextBtn.style.display = 'block';
    }}

    function loadNextQuestion() {{
        currentIdx++;
        if (currentIdx < TOTAL_QUESTIONS) renderQuestion();
        else finishExam();
    }}

    function finishExam() {{
        clearInterval(timerInterval);
        document.getElementById('exam-ui').style.display = 'none';
        const resultScreen = document.getElementById('result-screen');
        resultScreen.style.display = 'block';
        
        const percentage = (correctAnswers / TOTAL_QUESTIONS) * 100;
        document.getElementById('final-score').innerText = `Final Score: ${{correctAnswers}} / ${{TOTAL_QUESTIONS}} (${{percentage.toFixed(1)}}%)`;
        document.getElementById('final-time').innerText = `Time elapsed: ${{document.getElementById('timer').innerText}}`;
        
        const msgEl = document.getElementById('final-message');
        if (percentage >= 70) {{ 
            msgEl.innerText = "🎉 PASS! You demonstrate a solid understanding of Qiskit v2.x.";
            msgEl.style.color = "#24a148";
        }} else {{
            msgEl.innerText = "⚠️ FAIL. Review the V2 Primitives and ISA transpilation before taking the real exam.";
            msgEl.style.color = "#da1e28";
        }}
    }}

    window.onload = startExam;
</script>
</body>
</html>
"""
    
    html_path = os.path.abspath(html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args): pass 

    print("\n" + "="*60)
    print("✅ Exam generated successfully!")
    print(f"👉 To take the exam, click this link (or copy/paste it into Chrome):")
    print(f"\n    http://localhost:{{port}}/{{html_filename}}\n")
    print("Press Ctrl+C to stop the server when you are done.")
    print("="*60 + "\n")

    import webbrowser
    
    # Intento de apertura automática con Chrome u OS Default
    file_url = f"http://localhost:{{port}}/{{html_filename}}"
    chrome_opened = False
    chrome_paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe %s",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s",
        "chrome"
    ]
    for path in chrome_paths:
        try:
            webbrowser.get(path).open(file_url)
            chrome_opened = True
            break
        except webbrowser.Error: continue
            
    if not chrome_opened:
        webbrowser.open(file_url)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped. Good luck with your certification!")

if __name__ == "__main__":
    create_and_serve_html_exam()
