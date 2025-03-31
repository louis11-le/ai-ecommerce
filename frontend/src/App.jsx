import axios from 'axios';
import { useState } from 'react';
import React from 'react';

import ChatMessage from './components/ChatMessage';

function App() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;
    // Append user message to chat history
    const newMessages = [...messages, { role: 'user', text: question }];
    setMessages(newMessages);
    setQuestion('');

    try {
      // Call backend API (adjust URL if necessary)
      const response = await axios.post('http://localhost:8000/ask', {
        question,
      });
      setMessages([
        ...newMessages,
        { role: 'assistant', text: response.data.answer },
      ]);
    } catch (error) {
      console.error('Error calling API:', error);
      setMessages([
        ...newMessages,
        { role: 'assistant', text: 'Error: Unable to get response.' },
      ]);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6">AI E-commerce Assistant</h1>
      <div className="w-full max-w-2xl bg-white rounded shadow p-4 mb-4 space-y-4">
        {messages.map((msg, index) => (
          <ChatMessage key={index} role={msg.role} text={msg.text} />
        ))}
      </div>
      <div className="flex w-full max-w-2xl">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your question..."
          className="flex-grow border rounded-l px-4 py-2"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              askQuestion();
            }
          }}
        />
        <button
          onClick={askQuestion}
          className="bg-blue-500 text-white px-4 py-2 rounded-r"
        >
          Ask
        </button>
      </div>
    </div>
  );
}

export default App;
