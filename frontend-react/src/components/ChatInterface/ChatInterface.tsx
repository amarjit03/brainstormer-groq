import React, { useState, KeyboardEvent } from 'react';
import styles from './ChatInterface.module.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');

  const handleSendMessage = () => {
    if (inputText.trim() === '') return;

    const newUserMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
    };

    // Add user message
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);

    // Simulate bot echoing the message
    const botMessage: Message = {
      id: (Date.now() + 1).toString(), // Ensure unique ID
      text: `Echo: ${inputText}`,
      sender: 'bot',
    };

    // Add bot message after a short delay
    setTimeout(() => {
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }, 500);

    setInputText(''); // Clear input field
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messageList}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`${styles.message} ${
              msg.sender === 'user' ? styles.userMessage : styles.botMessage
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className={styles.inputArea}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
          className={styles.textInput}
        />
        <button onClick={handleSendMessage} className={styles.sendButton}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
