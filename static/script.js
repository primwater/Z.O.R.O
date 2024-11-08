// Function to display messages in the chat box
function displayMessage(message, isUser) {
  const chatBox = document.getElementById("chat-box");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", isUser ? "user" : "bot");
  messageDiv.innerHTML = formatMessage(message);
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Format the message to highlight code blocks
function formatMessage(message) {
  // Match content inside triple backticks (```) and wrap it in a code block with a copy button
  return message.replace(/```(.*?)```/gs, (match, code) => {
    return `<div class="language-tag">Python</div><pre><code>${escapeHtml(code.trim())}</code></pre><button class="copy-button" onclick="copyCode('${escapeHtml(code.trim())}')">Copy Code</button>`;
  });
}

// Function to escape special characters for inserting into HTML
function escapeHtml(text) {
  return text.replace(/[&<>"'`]/g, (match) => {
    const escapeMap = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;',
      '`': '&#96;',
    };
    return escapeMap[match];
  });
}

// Copy code to clipboard
function copyCode(code) {
  navigator.clipboard.writeText(code).then(() => {
    alert("Code copied to clipboard!");
  });
}

// Send message to backend and display response
function sendMessage() {
  const inputField = document.getElementById("user-input");
  const message = inputField.value;
  if (message.trim() === "") return;
  
  displayMessage(message, true); // User message
  
  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  })
    .then((response) => response.json())
    .then((data) => {
      displayMessage(data.response, false); // Bot response
    });

  inputField.value = "";
}
