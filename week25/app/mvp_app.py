"""
AI Learning Platform MVP - Week25
A minimal Flask app demonstrating the core user flow with event instrumentation.

Core Flow:
1. Open app → log app_open
2. Ask question → log question_submitted
3. Receive AI help → log answer_received
4. Mark Helpful/Not Helpful → log helpful_marked or feedback_submitted
5. Continue learning → log continue_learning_clicked
"""

from flask import Flask, render_template_string, request, jsonify, session
import time
import uuid
from analytics.event_logger import EventLogger

app = Flask(__name__)
app.secret_key = "week25_mvp_secret_key"

# Initialize event logger
logger = EventLogger(logfile="events.log")


# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Learning Helper</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #333; margin-bottom: 10px; text-align: center; }
        .subtitle { color: #666; text-align: center; margin-bottom: 30px; }
        .btn {
            display: block;
            width: 100%;
            padding: 15px 30px;
            margin: 10px 0;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(0,0,0,0.2); }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-success { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
        .btn-danger { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); color: white; }
        .btn-secondary { background: #e0e0e0; color: #333; }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            resize: vertical;
            min-height: 120px;
            margin-bottom: 20px;
        }
        textarea:focus { outline: none; border-color: #667eea; }
        .answer-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }
        .feedback-section { margin-top: 20px; }
        .hidden { display: none; }
        .status { 
            text-align: center; 
            padding: 10px; 
            border-radius: 8px; 
            margin: 10px 0;
        }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        @media (max-width: 480px) {
            .container { padding: 20px; }
            h1 { font-size: 24px; }
        }
    </style>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

HOME_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<h1>🎓 AI Learning Helper</h1>
<p class="subtitle">Get instant help with your questions</p>

<button class="btn btn-primary" onclick="location.href='/ask'">
    📝 Ask a Question
</button>

<button class="btn btn-secondary" onclick="location.href='/flow'">
    📊 View User Flow
</button>

<button class="btn btn-secondary" onclick="location.href='/analytics'">
    📈 View Analytics
</button>
{% endblock %}
"""

ASK_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<h1>📝 Ask a Question</h1>
<p class="subtitle">What would you like to learn about?</p>

<form id="questionForm" method="POST" action="/submit">
    <textarea 
        name="question" 
        placeholder="Type your question here... e.g., 'How do I solve quadratic equations?'"
        required
    ></textarea>
    <button type="submit" class="btn btn-primary">🚀 Get Help</button>
</form>

<a href="/" class="btn btn-secondary" style="text-decoration:none; text-align:center;">
    ← Back to Home
</a>
{% endblock %}
"""

ANSWER_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<h1>✅ Answer Received</h1>

<div class="answer-box">
    <strong>Your Question:</strong>
    <p>{{ question }}</p>
</div>

<div class="answer-box">
    <strong>AI Helper Response:</strong>
    <p>{{ answer }}</p>
</div>

<p class="subtitle">Was this helpful?</p>

<div class="feedback-section">
    <button class="btn btn-success" onclick="submitFeedback('helpful')">
        👍 Yes, Helpful!
    </button>
    <button class="btn btn-danger" onclick="submitFeedback('not_helpful')">
        👎 Not Helpful
    </button>
</div>

<button class="btn btn-primary" onclick="location.href='/ask'" style="margin-top: 20px;">
    ➡️ Continue Learning
</button>

<a href="/" class="btn btn-secondary" style="text-decoration:none; text-align:center; display:block; margin-top:10px;">
    ← Back to Home
</a>

<script>
function submitFeedback(type) {
    fetch('/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({feedback_type: type})
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert('Thank you for your feedback!');
        }
    });
}
</script>
{% endblock %}
"""

FLOW_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<h1>📊 User Flow</h1>
<p class="subtitle">Core learning journey with instrumentation points</p>

<div style="background:#f8f9fa; padding:20px; border-radius:12px; margin:20px 0;">
    <ol style="line-height:2.5; color:#333;">
        <li><strong>Open App</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">app_open</code></li>
        <li><strong>Tap "Ask Question"</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">help_button_clicked</code></li>
        <li><strong>Question Input Shown</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">question_input_shown</code></li>
        <li><strong>Submit Question</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">question_submitted</code></li>
        <li><strong>Backend Processes</strong> (internal)</li>
        <li><strong>Answer Displayed</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">answer_received</code></li>
        <li><strong>Mark Feedback</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">helpful_marked</code> or <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">feedback_submitted</code></li>
        <li><strong>Continue Learning</strong> → <code style="background:#e0e0e0;padding:2px 6px;border-radius:4px;">continue_learning_clicked</code></li>
    </ol>
</div>

<a href="/" class="btn btn-primary" style="text-decoration:none; text-align:center;">
    ← Back to Home
</a>
{% endblock %}
"""

ANALYTICS_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<h1>📈 Analytics Dashboard</h1>
<p class="subtitle">Recent events from this session</p>

<div style="background:#f8f9fa; padding:20px; border-radius:12px; margin:20px 0;">
    <h3>Session ID: {{ session_id }}</h3>
    <p>Events logged: {{ event_count }}</p>
    
    {% if events %}
    <div style="margin-top:20px; max-height:400px; overflow-y:auto;">
        {% for event in events %}
        <div style="background:white; padding:10px; margin:5px 0; border-radius:8px; font-family:monospace; font-size:12px;">
            {{ event }}
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="color:#666; margin-top:20px;">No events logged yet. Start using the app!</p>
    {% endif %}
</div>

<a href="/" class="btn btn-primary" style="text-decoration:none; text-align:center;">
    ← Back to Home
</a>
{% endblock %}
"""


def get_session_id():
    """Get or create session ID."""
    if 'session_id' not in session:
        session['session_id'] = f"sess_{uuid.uuid4().hex[:8]}"
        # Log app_open event
        logger.log_event({
            "event_name": "app_open",
            "timestamp": time.time(),
            "session_id": session['session_id'],
            "properties": {"source": "web"},
        })
    return session['session_id']


@app.route('/')
def home():
    """Home page."""
    get_session_id()  # Ensure session and log app_open
    return render_template_string(HOME_TEMPLATE)


@app.route('/ask')
def ask():
    """Ask question page."""
    session_id = get_session_id()
    # Log help_button_clicked
    logger.log_event({
        "event_name": "help_button_clicked",
        "timestamp": time.time(),
        "session_id": session_id,
    })
    # Log question_input_shown
    logger.log_event({
        "event_name": "question_input_shown",
        "timestamp": time.time(),
        "session_id": session_id,
    })
    return render_template_string(ASK_TEMPLATE)


@app.route('/submit', methods=['POST'])
def submit():
    """Submit question and show answer."""
    session_id = get_session_id()
    question = request.form.get('question', 'No question provided')
    
    # Log question_submitted
    logger.log_event({
        "event_name": "question_submitted",
        "timestamp": time.time(),
        "session_id": session_id,
        "properties": {"question_length": len(question)},
    })
    
    # Simulate AI response (in real app, this would call an AI API)
    answer = f"This is a simulated AI response to: '{question[:50]}...' \n\nIn a production environment, this would connect to an AI model to provide personalized learning assistance."
    
    # Log answer_received
    logger.log_event({
        "event_name": "answer_received",
        "timestamp": time.time(),
        "session_id": session_id,
        "properties": {"answer_length": len(answer)},
    })
    
    # Store in session for feedback
    session['last_question'] = question
    session['last_answer'] = answer
    
    return render_template_string(ANSWER_TEMPLATE, question=question, answer=answer)


@app.route('/feedback', methods=['POST'])
def feedback():
    """Handle feedback submission."""
    session_id = get_session_id()
    data = request.get_json() or {}
    feedback_type = data.get('feedback_type', 'unknown')
    
    if feedback_type == 'helpful':
        # Log helpful_marked
        logger.log_event({
            "event_name": "helpful_marked",
            "timestamp": time.time(),
            "session_id": session_id,
            "properties": {"rating": 5},
        })
        return jsonify({"success": True, "message": "Thanks for the positive feedback!"})
    else:
        # Log feedback_submitted
        logger.log_event({
            "event_name": "feedback_submitted",
            "timestamp": time.time(),
            "session_id": session_id,
            "properties": {"type": "not_helpful"},
        })
        return jsonify({"success": True, "message": "Thanks for your feedback!"})


@app.route('/continue')
def continue_learning():
    """Continue learning - log event and redirect."""
    session_id = get_session_id()
    
    # Log continue_learning_clicked
    logger.log_event({
        "event_name": "continue_learning_clicked",
        "timestamp": time.time(),
        "session_id": session_id,
    })
    
    return redirect('/ask')


@app.route('/flow')
def flow():
    """Show user flow documentation."""
    get_session_id()
    return render_template_string(FLOW_TEMPLATE)


@app.route('/analytics')
def analytics():
    """Show analytics for current session."""
    session_id = get_session_id()
    
    # Read recent events for this session
    events = []
    try:
        with open('events.log', 'r') as f:
            for line in f:
                if session_id in line:
                    events.append(line.strip())
    except FileNotFoundError:
        pass
    
    return render_template_string(
        ANALYTICS_TEMPLATE,
        session_id=session_id,
        event_count=len(events),
        events=events[-20:]  # Last 20 events
    )


if __name__ == '__main__':
    print("=" * 60)
    print("AI Learning Platform MVP - Week25")
    print("=" * 60)
    print("\nStarting server...")
    print("Open http://localhost:5000 in your browser")
    print("\nCore Flow:")
    print("1. Open app → Ask question → Receive AI help")
    print("2. Mark Helpful / Not Helpful")
    print("3. Events automatically logged to events.log")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
