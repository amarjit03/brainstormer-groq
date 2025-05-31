import React from 'react';
import './App.css'; // Keep or modify as needed
import ChatInterface from './components/ChatInterface/ChatInterface';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>React Chat App</h1>
      </header>
      <main>
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
