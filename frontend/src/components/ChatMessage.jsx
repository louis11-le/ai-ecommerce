import React from 'react';

const ChatMessage = ({ role, text }) => {
  const isUser = role === 'user';
  return (
    <div
      className={`p-3 my-2 rounded ${isUser ? 'bg-gray-200 self-end' : 'bg-blue-100 self-start'}`}
    >
      <strong>{isUser ? 'You' : 'Assistant'}:</strong>
      <p>{text}</p>
    </div>
  );
};

export default ChatMessage;
