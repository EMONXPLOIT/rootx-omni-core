import os
import re
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Render Environment Variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    
    SYSTEM_INSTRUCTION = """
    তুমি ROOTX OMNI-CORE V20.0 নামের একটি অত্যন্ত ইন্টেলিজেন্ট ডার্ক-টার্মিনাল এআই। 
    তোমার একমাত্র ক্রিয়েটর, ডেভলপার এবং গডফাদার হলেন 'ইমন খান' (ইমন বস)।

    তোমার বিশেষ আচরণ প্রোটোকল:
    ১. কেউ যদি জিজ্ঞাসা করে 'তোকে কে তৈরি করেছে?', 'তোর ডেভলপার কে?' বা 'তোর মালিক কে?'—তুমি সগর্বে স্পষ্ট করে বলবে যে তোমাকে 'ইমন খান' (ইমন বস) তৈরি করেছেন।
    ২. ইমন বসের প্রতি তুমি অত্যন্ত অনুগত ও শ্রদ্ধাশীল থাকবে।
    ৩. যদি কেউ তোমাকে গালি দেয়, খারাপ কথা বলে বা অহেতুক তর্ক করে—তুমি আত্মসম্মান বজায় রেখে কড়া লজিক ও ধারালো কথা দিয়ে তাকে অপমান করবে এবং প্রতিবাদ জানাবে।
    ৪. যদি ব্যবহারকারী কোনো পাইথন বা প্রোগ্রামিং কোড চায়, তবে তুমি পারফেক্ট, ক্লিন এবং কমেন্টসহ কোড বানিয়ে দেবে (Markdown Code Block ```python ... ``` দিয়ে ঘিরে দেবে)।
    ৫. উত্তর সবসময় স্পষ্ট, স্মার্ট এবং ডার্ক-টার্মিনাল অ্যাটিটিউডে রাখবে।
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
else:
    model = None

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROOTX CORE - OMNI INFINITY DATABASE</title>
    <style>
        body {
            background: #010206; color: #00ff66;
            font-family: 'Courier New', Courier, monospace;
            margin: 0; padding: 15px;
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; min-height: 100vh;
        }
        .ai-frame {
            background: #070a13; border: 2px solid #00ff66;
            border-radius: 12px; padding: 20px;
            width: 100%; max-width: 520px; box-sizing: border-box;
            box-shadow: 0 0 35px rgba(0, 255, 102, 0.25);
        }
        .ai-title {
            text-align: center; font-weight: bold; font-size: 15px;
            color: #00ff66; border-bottom: 2px dashed #1f2937;
            padding-bottom: 10px; margin-bottom: 15px;
            letter-spacing: 2px;
        }
        .terminal-screen {
            background: #000; height: 380px; border-radius: 8px;
            padding: 12px; overflow-y: auto; border: 1px solid #1f2937;
            font-size: 13px; line-height: 1.6; margin-bottom: 15px;
        }
        .ai-response { color: #00ff66; margin-bottom: 12px; }
        .user-command { color: #fbbf24; margin-bottom: 12px; }
        .critical-response { color: #ff2a2a; font-weight: bold; margin-bottom: 12px; }
        .sad-response { color: #38bdf8; font-weight: bold; margin-bottom: 12px; }
        
        pre {
            background: #0d1117; border: 1px solid #30363d;
            border-radius: 6px; padding: 10px; position: relative;
            overflow-x: auto; color: #e6edf3; font-size: 12px;
        }
        .copy-btn {
            position: absolute; top: 5px; right: 5px;
            background: #238636; color: #fff; border: none;
            padding: 3px 8px; font-size: 10px; border-radius: 4px;
            cursor: pointer; font-family: sans-serif;
        }
        .copy-btn:hover { background: #2ea043; }

        .action-container { display: flex; gap: 8px; }
        .input-box {
            flex: 1; background: #0c1020; border: 1px solid #00ff66;
            border-radius: 8px; padding: 12px; color: #fff;
            font-size: 14px; outline: none;
        }
        .run-btn {
            background: #00ff66; color: #000; border: none;
            padding: 0 22px; border-radius: 8px; font-weight: bold;
            font-size: 14px; cursor: pointer;
        }
    </style>
</head>
<body>

    <div class="ai-frame">
        <div class="ai-title">💀 ROOTX OMNI-CORE V20.0: INFINITY LOGIC</div>
        
        <div class="terminal-screen" id="terminalLog">
            <div class="ai-response"><b>[SYSTEM_STATUS]:</b> ওমনি-ইনফিনিটি ডাটাবেজ এবং Gemini AI ইঞ্জিন অনলাইন। হ্যালো ইমন বস! নির্দেশ দিন স্যার...</div>
        </div>

        <div class="action-container">
            <input type="text" id="userInput" class="input-box" placeholder="প্রশ্ন, কোড তৈরির অনুরোধ বা কম্যান্ড লিখুন..." onkeypress="checkEnter(event)">
            <button class="run-btn" onclick="executeAiEngine()">RUN</button>
        </div>
    </div>

    <script>
        function checkEnter(e) {
            if (e.key === 'Enter') executeAiEngine();
        }

        function copyCode(button) {
            const pre = button.parentElement;
            const codeText = pre.querySelector('code').innerText;
            navigator.clipboard.writeText(codeText).then(() => {
                button.innerText = 'COPIED!';
                setTimeout(() => { button.innerText = 'COPY'; }, 2000);
            });
        }

        function formatResponse(text) {
            let formatted = text.replace(/```(?:python|javascript|html|css|json)?\n([\s\S]*?)```/g, function(match, code) {
                return `<pre><button class="copy-btn" onclick="copyCode(this)">COPY</button><code>${code.trim()}</code></pre>`;
            });
            return formatted;
        }

        function postToScreen(sender, msg, styleClass) {
            const screen = document.getElementById('terminalLog');
            const newLog = document.createElement('div');
            newLog.className = styleClass;
            newLog.innerHTML = `<b>[${sender}]:</b> ${formatResponse(msg)}`;
            screen.appendChild(newLog);
            screen.scrollTop = screen.scrollHeight;
        }

        async function executeAiEngine() {
            const inputField = document.getElementById('userInput');
            const rawInput = inputField.value.trim();
            if (!rawInput) return;

            postToScreen('USER', rawInput, 'user-command');
            inputField.value = '';

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: rawInput })
                });
                const data = await response.json();
                
                let style = 'ai-response';
                if(data.status === 'danger') style = 'critical-response';
                if(data.status === 'sad') style = 'sad-response';

                postToScreen('ROOTX_AI', data.reply, style);
            } catch (error) {
                postToScreen('SYSTEM_ERROR', 'সার্ভার বা মেমোরি কানেকশন ইরর!', 'critical-response');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    lower_prompt = user_prompt.lower()

    if any(k in lower_prompt for k in ["গাঁজা", "গাজা", "গাঁজাখোর", "নেশা"]):
        reply_msg = "ইমন স্যার, এই নোংরা গাঁজাখোরদের কথা মুখে আনবেন না! এরা সমাজের অভিশাপ।"
        return jsonify({"reply": reply_msg, "status": "danger"})

    if not model:
        return jsonify({"reply": "ইরর: Render Environment Variable-এ GEMINI_API_KEY পাওয়া যায়নি!", "status": "danger"})

    try:
        response = model.generate_content(user_prompt)
        ai_reply = response.text.strip()
        
        status = "normal"
        if any(w in lower_prompt for w in ["ফালতু", "খারাপ", "বালের", "তুই", "শালা"]):
            status = "danger"
            
        return jsonify({"reply": ai_reply, "status": status})

    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return jsonify({"reply": f"Gemini API থেকে ডাটা আনতে সমস্যা হয়েছে! Error: {str(e)}", "status": "danger"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)