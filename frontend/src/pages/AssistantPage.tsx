import React, { useState } from 'react';
import { sendAssistantChat } from '../services/api';
import { AssistantChatResult } from '../types';
import { Bot, Send, User, Sparkles, BookOpen, ShieldAlert, CornerDownLeft } from 'lucide-react';

interface ChatMessage {
  sender: 'user' | 'assistant';
  text: string;
  standards?: string[];
  followups?: string[];
  timestamp: string;
}

export const AssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: 'assistant',
      text: (
        "Namaste! I am the RailRakshak AI Maintenance Assistant, trained to assist Permanent Way Engineers with " +
        "Indian Railways Permanent Way Manual (IRPWM 2020) standards, RDSO Ultrasonic Flaw Detection (USFD) defect codes, " +
        "CAG derailment causation analytics, and supervised machine learning metrics (INT395 Topic 20). " +
        "How may I assist your track inspection planning today?"
      ),
      standards: ["IRPWM 2020 Table 5.1", "RDSO USFD Manual", "CAG Report No. 22 of 2022"],
      followups: [
        "What are the IRPWM 2020 Urgent Maintenance Limits for speed ≥ 130 km/h?",
        "Explain Crosslevel vs Track Twist derailment risks",
        "What actions are mandated for an RDSO Code 111 IMR defect?",
        "Explain why Macro-F1 was chosen as the primary metric for INT395"
      ],
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [inputText, setInputText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSend = async (queryToSend?: string) => {
    const q = queryToSend || inputText;
    if (!q.trim()) return;

    const userMsg: ChatMessage = {
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res: AssistantChatResult = await sendAssistantChat(q);
      const assistantMsg: ChatMessage = {
        sender: 'assistant',
        text: res.response_text,
        standards: res.referenced_standards,
        followups: res.suggested_followups,
        timestamp: res.timestamp || new Date().toLocaleTimeString()
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        sender: 'assistant',
        text: "I encountered a communication error with the backend assistant engine. Please ensure the FastAPI server is active.",
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-xs">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold text-slate-900 tracking-tight">
                Module 16 — AI Railway Maintenance Assistant
              </h1>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                Domain Grounded
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Natural language technical advisory referencing IRPWM 2020, RDSO technical specifications, and ML models.
            </p>
          </div>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-[540px] overflow-hidden">
        <div className="flex-1 p-5 overflow-y-auto space-y-4">
          {messages.map((m, idx) => {
            const isUser = m.sender === 'user';
            return (
              <div key={idx} className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  isUser ? 'bg-slate-900 text-white' : 'bg-blue-600 text-white'
                }`}>
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                <div className={`max-w-[75%] rounded-xl p-4 text-xs leading-relaxed ${
                  isUser
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-none'
                }`}>
                  <p className="whitespace-pre-wrap">{m.text}</p>

                  {/* Standards Badges */}
                  {m.standards && m.standards.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap gap-1.5 items-center">
                      <span className="text-[10px] font-bold text-slate-400 flex items-center">
                        <BookOpen className="w-3 h-3 mr-1" />
                        Standards Referenced:
                      </span>
                      {m.standards.map((std, sidx) => (
                        <span key={sidx} className="px-2 py-0.5 rounded bg-white border border-slate-200 font-mono text-[10px] text-slate-700">
                          {std}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Follow-up Chips */}
                  {m.followups && m.followups.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-slate-200 space-y-1.5">
                      <span className="text-[10px] font-bold text-slate-400 flex items-center">
                        <Sparkles className="w-3 h-3 mr-1 text-blue-600" />
                        Suggested Inquiries:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {m.followups.map((chip, cidx) => (
                          <button
                            key={cidx}
                            onClick={() => handleSend(chip)}
                            className="text-left text-[11px] px-2.5 py-1 rounded-md bg-white hover:bg-blue-50 hover:text-blue-700 border border-slate-200 text-slate-700 font-medium transition-colors"
                          >
                            {chip}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className={`mt-1.5 text-[9px] text-right ${isUser ? 'text-blue-200' : 'text-slate-400'}`}>
                    {m.timestamp}
                  </div>
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="flex items-center space-x-2 text-xs text-slate-400 pl-11">
              <Bot className="w-4 h-4 animate-spin text-blue-600" />
              <span>Consulting IRPWM 2020 standards knowledge base...</span>
            </div>
          )}
        </div>

        {/* Input Field */}
        <div className="p-3 border-t border-slate-200 bg-slate-50 flex items-center space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about IRPWM geometry limits, USFD flaw codes, or model metrics..."
            className="flex-1 px-4 py-2.5 bg-white border border-slate-200 rounded-lg text-xs text-slate-800 focus:outline-hidden focus:ring-1 focus:ring-blue-500 shadow-2xs"
          />
          <button
            onClick={() => handleSend()}
            disabled={loading || !inputText.trim()}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg text-xs font-semibold flex items-center shadow-xs transition-colors"
          >
            <span>Send</span>
            <Send className="w-3.5 h-3.5 ml-1.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
