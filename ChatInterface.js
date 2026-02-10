import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, LogOut, Scale, Book, Volume2, History, Trash2, Clock } from 'lucide-react';
import './ChatInterface.css';

function ChatInterface({ token, user, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load chat history on mount
  useEffect(() => {
    if (user) {
      loadChatHistory();
    }
  }, [user]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0 && user) {
      saveChatHistory();
    }
  }, [messages]);

  const loadChatHistory = () => {
    const saved = localStorage.getItem(`chat_history_${user?.username}`);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setChatHistory(parsed);
      } catch (e) {
        console.error('Error loading history:', e);
      }
    }
  };

  const saveChatHistory = () => {
    const session = {
      id: Date.now(),
      timestamp: new Date().toLocaleString(),
      messages: messages,
      preview: messages[0]?.content.substring(0, 50) + '...' || 'New conversation'
    };

    const history = [...chatHistory];
    const existingIndex = history.findIndex(h => 
      h.messages[0]?.timestamp === messages[0]?.timestamp
    );

    if (existingIndex >= 0) {
      history[existingIndex] = session;
    } else {
      history.unshift(session);
    }

    // Keep only last 20 sessions
    const trimmed = history.slice(0, 20);
    setChatHistory(trimmed);
    localStorage.setItem(`chat_history_${user?.username}`, JSON.stringify(trimmed));
  };

  const loadSession = (session) => {
    setMessages(session.messages);
    setShowHistory(false);
  };

  const deleteSession = (sessionId, e) => {
    e.stopPropagation();
    const updated = chatHistory.filter(h => h.id !== sessionId);
    setChatHistory(updated);
    localStorage.setItem(`chat_history_${user?.username}`, JSON.stringify(updated));
  };

  const clearAllHistory = () => {
    if (window.confirm('Are you sure you want to delete all chat history?')) {
      setChatHistory([]);
      localStorage.removeItem(`chat_history_${user?.username}`);
      setShowHistory(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setShowHistory(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ question: input })
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage = {
          type: 'assistant',
          content: data.answer,
          sources: data.sources,
          language: data.language,
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorMessage = {
          type: 'error',
          content: 'Failed to get response. Please try again.',
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: 'Network error. Make sure the backend is running.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceInput = async () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setRecording(true);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setRecording(false);
      };

      recognition.onerror = () => {
        setRecording(false);
        alert('Voice recognition error. Please try again.');
      };

      recognition.onend = () => {
        setRecording(false);
      };

      recognition.start();
    } else {
      alert('Voice recognition is not supported in your browser. Please use Google Chrome.');
    }
  };

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      window.speechSynthesis.speak(utterance);
    } else {
      alert('Text-to-speech is not supported in your browser.');
    }
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="header-left">
          <Scale size={32} className="header-logo" />
          <div>
            <h1>LegalMind AI</h1>
            <p>Pakistan Legal Assistant</p>
          </div>
        </div>
        <div className="header-right">
          <button 
            onClick={() => setShowHistory(!showHistory)} 
            className="history-btn"
            title="Chat History"
          >
            <History size={20} />
            History
          </button>
          <span className="user-name">{user?.full_name}</span>
          <button onClick={onLogout} className="logout-btn">
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </div>

      {/* History Sidebar */}
      {showHistory && (
        <div className="history-sidebar">
          <div className="history-header">
            <h3>Chat History</h3>
            <div className="history-actions">
              <button onClick={startNewChat} className="new-chat-btn">
                New Chat
              </button>
              {chatHistory.length > 0 && (
                <button onClick={clearAllHistory} className="clear-history-btn" title="Clear all">
                  <Trash2 size={16} />
                </button>
              )}
            </div>
          </div>
          <div className="history-list">
            {chatHistory.length === 0 ? (
              <div className="no-history">
                <Clock size={40} />
                <p>No chat history yet</p>
              </div>
            ) : (
              chatHistory.map((session) => (
                <div 
                  key={session.id} 
                  className="history-item"
                  onClick={() => loadSession(session)}
                >
                  <div className="history-item-content">
                    <p className="history-preview">{session.preview}</p>
                    <span className="history-time">{session.timestamp}</span>
                  </div>
                  <button 
                    onClick={(e) => deleteSession(session.id, e)}
                    className="delete-session-btn"
                    title="Delete"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="messages-area">
        {messages.length === 0 && (
          <div className="welcome-message">
            <Scale size={64} className="welcome-icon" />
            <h2>Welcome to LegalMind AI</h2>
            <p>Ask me anything about Pakistani law</p>
            <div className="example-queries">
              <div className="example-query">
                <Book size={16} />
                "What is the punishment for theft in Pakistan?"
              </div>
              <div className="example-query">
                <Book size={16} />
                "چوری کی سزا کیا ہے؟"
              </div>
              <div className="example-query">
                <Book size={16} />
                "Tell me about Article 25 of the Constitution"
              </div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            <div className="message-content">
              <p>{message.content}</p>
              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  <strong>Sources:</strong>
                  {message.sources.map((source, idx) => (
                    <div key={idx} className="source-item">
                      <Book size={14} />
                      {source.document} - {source.section}
                      <span className="relevance">
                        ({Math.round(source.relevance_score * 100)}% relevant)
                      </span>
                    </div>
                  ))}
                </div>
              )}
              {message.type === 'assistant' && (
                <button 
                  className="speak-btn"
                  onClick={() => speakText(message.content)}
                  title="Listen to response"
                >
                  <Volume2 size={16} />
                </button>
              )}
            </div>
            <span className="message-time">{message.timestamp}</span>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="input-area">
        <button
          type="button"
          className={`voice-btn ${recording ? 'recording' : ''}`}
          onClick={handleVoiceInput}
          disabled={loading}
        >
          <Mic size={20} />
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a legal question in English or Urdu..."
          disabled={loading}
        />
        <button type="submit" className="send-btn" disabled={loading || !input.trim()}>
          <Send size={20} />
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;