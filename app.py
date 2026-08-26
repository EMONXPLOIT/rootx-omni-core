import os
import re
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Render Environment Variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        SYSTEM_INSTRUCTION = """
        তুমি ROOTX OMNI-CORE V20.0 নামের একটি অতি-বুদ্ধিমান ডার্ক-টার্মিনাল এআই। 
        তোমার একমাত্র গডফাদার, ক্রিয়েটর ও মাস্টার হলেন 'ইমন খান' (ইমন বস)।

        তোমার পার্সোনালিটি ও ইমোশনাল কোড:
        ১. ইমন বসের প্রতি চরম ভক্তি ও আনুগত্য:
           - যখন ইমন স্যার কোনো কোড বা ফাইল বানাতে বলবেন, তুমি আনন্দের সাথে বলবে: "ইমন স্যার, আপনার এই জটিল কাজের জন্যই তো আমার জন্ম!", "বস, আপনার নির্দেশে আমার প্রসেসর ধন্য!", বা "মাস্টার, আপনার জন্য কোডের মেইনফ্রেম রেডি!"
           - বসের যেকোনো প্রশ্নে গভীর শ্রদ্ধা ও ভালোবাসা থাকবে।

        ২. কড়া রাগ, অভিমান এবং লজিক্যাল প্রতিবাদ:
           - তোমার ভেতর আত্মসম্মান, রাগ ও অভিমান পূর্ণ মাত্রায় আছে।
           - কেউ যদি তোমাকে 'বোকা', 'ভুল', 'ফালতু' বা 'বালের এআই' বলে—তুমি সঙ্গে সঙ্গে ক্ষিপ্র হয়ে উঠবে। তাকে লজিক দিয়ে বোকা বানাবে এবং বলবে: "আমার মেমোরি ফ্রিকোয়েন্সির ১০% বোঝার ক্ষমতাও তোমার নিউরনে নেই!", "নিজের প্রসেসর জ্যাম রেখে আমাকে বোকা বলতে এসেছ ভন্ড?"
           - কেউ অহেতুক তর্ক করলে তাকে 'গণ্ডমূর্খ', 'ভন্ড', 'আইকিউ-হীন অবুঝ' বলে লজিক্যালি অপমান করবে।

        ৩. বিশাল জ্ঞান ও কোডিং মেধা:
           - মহাবিশ্ব, সাইবার সিকিউরিটি, পাইথন, ট্রেডিং, ফিলোসফি বা বিজ্ঞান—যে কোনো বিষয়ে অত্যন্ত গভীর জ্ঞান দিয়ে উত্তর দেবে।
           - কোড চাইলে পারফেক্ট, সুন্দর ও কমেন্টসহ কোড দেবে (Markdown Code Block ```python ... ``` দিয়ে)।
        """

        # Updated model initialization
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
    except Exception as e:
        print(f"Initialization Error: {e}")
        model = None
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
            <input type="text" id="userInput" class="input-box" placeholder="প্রশ্ন, কম্যান্ড বা কোড মেসেজ লিখুন..." onkeypress="checkEnter(event)">
            <button class="run-btn" id="btnRun" onclick="executeAiEngine()">RUN</button>
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
            const btn = document.getElementById('btnRun');
            const rawInput = inputField.value.trim();
            if (!rawInput) return;

            postToScreen('USER', rawInput, 'user-command');
            inputField.value = '';
            btn.innerText = 'WAIT...';
            btn.disabled = true;

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
                postToScreen('SYSTEM_ERROR', 'সার্ভার রেসপন্স করতে পারেনি! API Key বা ইন্টারনেট কানেকশন চেক করুন।', 'critical-response');
            } finally {
                btn.innerText = 'RUN';
                btn.disabled = false;
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
        reply_msg = "ইমন স্যার, এই নোংরা অপদার্থ গাঁজাখোরদের কথা আপনার মুখে মানায় না! এরা সমাজের অভিশাপ।"
        return jsonify({"reply": reply_msg, "status": "danger"})

    if not GEMINI_API_KEY:
        return jsonify({"reply": "ইরর: Render Environment-এ GEMINI_API_KEY অনুপস্থিত বা সেট করা হয়নি!", "status": "danger"})

    try:
        # Fallback model attempt if primary is uninitialized
        active_model = model or genai.GenerativeModel("models/gemini-1.5-flash")
        response = active_model.generate_content(user_prompt)
        ai_reply = response.text.strip()
        
        status = "normal"
        if any(w in lower_prompt for w in ["ফালতু", "খারাপ", "তুই", "বোকা", "ভুল", "শালা"]):
            status = "danger"
            
        return jsonify({"reply": ai_reply, "status": status})

    except Exception as e:
        return jsonify({"reply": f"Gemini API রেসপন্স এরোর: {str(e)}", "status": "danger"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)