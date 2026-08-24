import os
import http.server
import socketserver

def create_and_serve_html_exam(db_path="qiskit_v2_database.json", html_filename="practice_exam_ui.html", port=8000):
    # 1. Leer la base de datos
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            questions_json = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{db_path}'. Ensure it is in the same directory.")
        return

    # 2. Plantilla HTML, CSS y JavaScript (Mantenemos tu diseño perfecto)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qiskit v2.x Certification Exam</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .exam-container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 800px; margin: 20px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f62fe; padding-bottom: 15px; margin-bottom: 20px; }}
        .header div {{ font-size: 1.1em; font-weight: bold; }}
        .stats {{ display: flex; gap: 20px; }}
        .stat-correct {{ color: #24a148; }}
        .stat-incorrect {{ color: #da1e28; }}
        .question-title {{ font-size: 1.2em; color: #0f62fe; margin-bottom: 10px; }}
        .question-text {{ font-size: 1.1em; margin-bottom: 25px; line-height: 1.5; white-space: pre-wrap; font-family: 'Consolas', 'Courier New', monospace; background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; }}
        .options {{ display: flex; flex-direction: column; gap: 10px; }}
        .option-btn {{ background-color: #f4f7f6; border: 2px solid #e0e0e0; padding: 15px; border-radius: 6px; font-size: 1em; cursor: pointer; text-align: left; transition: all 0.2s; font-family: 'Consolas', 'Courier New', monospace; white-space: pre-wrap; }}
        .option-btn:hover:not(:disabled) {{ background-color: #e5eaea; border-color: #0f62fe; }}
        .option-btn:disabled {{ cursor: not-allowed; }}
        .correct {{ background-color: #defbe6 !important; border-color: #24a148 !important; color: #198038; }}
        .incorrect {{ background-color: #fff1f1 !important; border-color: #da1e28 !important; color: #a2191f; }}
        .feedback {{ margin-top: 20px; padding: 15px; border-radius: 6px; background-color: #e5f6ff; border-left: 5px solid #0f62fe; display: none; }}
        .next-btn {{ margin-top: 25px; background-color: #0f62fe; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1em; cursor: pointer; float: right; display: none; }}
        .next-btn:hover {{ background-color: #0353e9; }}
        .result-screen {{ display: none; text-align: center; }}
        .result-screen h1 {{ color: #0f62fe; }}
        .clear {{ clear: both; }}
    </style>
</head>
<body>
<div class="exam-container" id="exam-ui">
    <div class="header">
        <div id="progress-text">Question 1 / 47</div>
        <div class="stats">
            <div>Time: <span id="timer">00:00</span></div>
            <div class="stat-correct">Correct: <span id="score-correct">0</span></div>
            <div class="stat-incorrect">Incorrect: <span id="score-incorrect">0</span></div>
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
    // El examen real de IBM exige unas 47 correctas de 68 (aprox 69%). Haremos el simulacro de 47 preguntas.
    const TOTAL_QUESTIONS = Math.min(47, db.length); 
    let examQuestions = [];
    let currentIdx = 0;
    let correctAnswers = 0;
    let incorrectAnswers = 0;
    let startTime;
    let timerInterval;

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
        if (percentage >= 69) {{ 
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
    
    # 3. Guardar el archivo HTML localmente
    html_path = os.path.abspath(html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 4. Iniciar un servidor local
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Silenciar los logs del servidor para una consola más limpia

    print("\n" + "="*60)
    print("✅ Exam generated successfully!")
    print(f"👉 To take the exam, click this link (or copy/paste it into Chrome):")
    print(f"\n    http://localhost:{port}/{html_filename}\n")
    print("Press Ctrl+C to stop the server when you are done.")
    print("="*60 + "\n")

    # Arrancar el servidor
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped. Good luck with your certification!")

if __name__ == "__main__":
    create_and_serve_html_exam()