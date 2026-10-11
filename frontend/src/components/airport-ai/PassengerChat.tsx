import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Compass, Clock, MapPin, AlertCircle, Luggage, Building, Sparkles } from 'lucide-react';
import { ChatMessage, FlightGuidance, Facility } from '../../types';
import { api } from '../../services/api';

interface PassengerChatProps {
  language: string;
}

export const PassengerChat: React.FC<PassengerChatProps> = ({ language }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'assistant',
      text: 'Welcome to TRAIT AirportAI! I am your real-time passenger assistant powered by a local knowledge base. You can ask about flight statuses (e.g. AI-204, 6E-531, BA-142), gate directions, baggage belts, lounge access, or security regulations.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const quickPrompts = [
    { label: '✈️ Status of AI-204', query: 'Status of flight AI-204' },
    { label: '🚪 Where is Gate 24B?', query: 'Where is Gate 24B and how long does it take to walk there?' },
    { label: '🧳 Baggage for 6E-531', query: 'Which baggage carousel is assigned to flight 6E-531?' },
    { label: '☕ Encalm Lounge info', query: 'Where is the Encalm Lounge and what are the access rules?' },
    { label: '💧 Liquids & 100ml rules', query: 'What are the security regulations for carrying liquids and electronics?' },
    { label: '🚌 Inter-terminal transfer', query: 'How do I transfer between Terminal 1, Terminal 2, and Terminal 3?' },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (queryText?: string) => {
    const textToSend = (queryText || input).trim();
    if (!textToSend || isLoading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInput('');
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage(textToSend, language);
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: response.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        language: response.detected_language,
        flightGuidance: response.flight_guidance,
        facilities: response.facility_matches,
        confidence: response.confidence,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: 'Sorry, I encountered an issue connecting to the local airport knowledge base. Please ensure the backend service is operational.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'On-Time': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'Delayed': return 'bg-rose-500/20 text-rose-400 border-rose-500/30';
      case 'Boarding': return 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30 animate-pulse';
      case 'Gate Closed': return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
      default: return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    }
  };

  return (
    <div className="flex flex-col h-[740px] bg-[#0E172E] rounded-2xl border border-[#1E2E4E] shadow-xl overflow-hidden">
      {/* Chat Header */}
      <div className="bg-[#121E3B] px-5 py-3.5 border-b border-[#1E2E4E] flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-md shadow-cyan-500/30">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-white text-sm">TRAIT Passenger Concierge</span>
              <span className="text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800/80 px-1.5 py-0.2 rounded font-mono">
                Local TF-IDF AI
              </span>
            </div>
            <div className="text-xs text-slate-400">Offline knowledge retrieval • Zero paid API cost</div>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Multilingual Active ({language.toUpperCase()})</span>
        </div>
      </div>

      {/* Message Stream */}
      <div className="flex-1 p-5 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start space-x-3 ${msg.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}
          >
            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-cyan-900/60 text-cyan-300 border border-cyan-700/50'
              }`}
            >
              {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Bubble Content */}
            <div className={`max-w-[82%] space-y-3`}>
              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-[#15223F] text-slate-200 border border-[#22355A] rounded-tl-none shadow-sm'
                }`}
              >
                <div className="whitespace-pre-line">{msg.text}</div>
                <div className="mt-1 text-[10px] text-right text-slate-400 font-mono">{msg.timestamp}</div>
              </div>

              {/* Rich Flight Guidance Card if attached */}
              {msg.flightGuidance && (
                <div className="bg-[#101B34] border border-cyan-800/40 rounded-xl p-4 shadow-lg text-xs space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-700/50">
                    <div className="flex items-center space-x-2">
                      <span className="text-base font-bold text-white font-mono">{msg.flightGuidance.flight_number}</span>
                      <span className="text-slate-400">({msg.flightGuidance.airline})</span>
                    </div>
                    <div className="flex items-center space-x-1.5">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${getStatusColor(msg.flightGuidance.status)}`}>
                        {msg.flightGuidance.status}
                      </span>
                      {msg.flightGuidance.delay_minutes > 0 && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                          +{msg.flightGuidance.delay_minutes}m ({msg.flightGuidance.delay_reason})
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Core Gate / Checkin / Carousel Grid */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-slate-300">
                    <div className="bg-[#18274A] p-2.5 rounded-lg border border-slate-700/40">
                      <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                        <Building className="w-3 h-3 text-cyan-400" />
                        <span>Terminal</span>
                      </div>
                      <div className="text-sm font-bold text-white mt-0.5">{msg.flightGuidance.terminal}</div>
                    </div>
                    <div className="bg-[#18274A] p-2.5 rounded-lg border border-slate-700/40">
                      <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                        <MapPin className="w-3 h-3 text-emerald-400" />
                        <span>Gate</span>
                      </div>
                      <div className="text-sm font-bold text-cyan-300 mt-0.5">{msg.flightGuidance.gate}</div>
                    </div>
                    <div className="bg-[#18274A] p-2.5 rounded-lg border border-slate-700/40">
                      <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                        <Clock className="w-3 h-3 text-amber-400" />
                        <span>Est. Departure</span>
                      </div>
                      <div className="text-xs font-bold text-slate-200 mt-1">{msg.flightGuidance.estimated_time}</div>
                    </div>
                    <div className="bg-[#18274A] p-2.5 rounded-lg border border-slate-700/40">
                      <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                        <Luggage className="w-3 h-3 text-purple-400" />
                        <span>Baggage Belt</span>
                      </div>
                      <div className="text-sm font-bold text-purple-300 mt-0.5">{msg.flightGuidance.baggage_carousel}</div>
                    </div>
                  </div>

                  {/* Turn-by-turn Navigation Steps */}
                  {msg.flightGuidance.navigation_steps.length > 0 && (
                    <div className="pt-2">
                      <div className="text-[11px] font-bold text-cyan-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                        <Compass className="w-3.5 h-3.5" />
                        <span>Turn-by-Turn Passenger Navigation</span>
                      </div>
                      <div className="space-y-1.5">
                        {msg.flightGuidance.navigation_steps.map((st) => (
                          <div
                            key={st.step_number}
                            className="flex items-start space-x-2.5 bg-[#14203D] p-2 rounded-lg border border-slate-800"
                          >
                            <span className="w-5 h-5 rounded-full bg-cyan-900 text-cyan-300 font-mono text-[10px] font-bold flex items-center justify-center shrink-0">
                              {st.step_number}
                            </span>
                            <div className="flex-1">
                              <p className="text-slate-200">{st.instruction}</p>
                              <div className="text-[10px] text-slate-400 mt-0.5 flex items-center space-x-2">
                                <span>~{st.estimated_minutes} min walk</span>
                                <span>•</span>
                                <span>{st.distance_meters} meters</span>
                                {st.landmark && (
                                  <>
                                    <span>•</span>
                                    <span className="text-amber-400/80">Landmark: {st.landmark}</span>
                                  </>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Quick Tips */}
                  {msg.flightGuidance.quick_tips.length > 0 && (
                    <div className="bg-amber-950/30 border border-amber-800/40 p-2.5 rounded-lg text-amber-200/90 text-[11px] space-y-1">
                      <div className="font-semibold flex items-center space-x-1">
                        <AlertCircle className="w-3 h-3 text-amber-400" />
                        <span>Passenger Advisories:</span>
                      </div>
                      <ul className="list-disc list-inside space-y-0.5 pl-1">
                        {msg.flightGuidance.quick_tips.map((tip, idx) => (
                          <li key={idx}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Matched Facilities Cards */}
              {msg.facilities && msg.facilities.length > 0 && !msg.flightGuidance && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  {msg.facilities.slice(0, 2).map((fac) => (
                    <div key={fac.id} className="bg-[#121E3A] border border-slate-700 p-2.5 rounded-lg space-y-1">
                      <div className="font-bold text-white flex items-center justify-between">
                        <span>{fac.name}</span>
                        <span className="text-[10px] bg-slate-800 text-cyan-400 px-1.5 py-0.5 rounded">{fac.terminal}</span>
                      </div>
                      <p className="text-slate-300 text-[11px]">{fac.location_desc}</p>
                      <div className="text-[10px] text-slate-400 flex items-center justify-between pt-1">
                        <span>Hours: {fac.opening_hours}</span>
                        <span>Walk: ~{fac.walking_time_mins}m</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center space-x-3 text-slate-400 text-xs">
            <div className="w-8 h-8 rounded-lg bg-cyan-900/60 text-cyan-300 border border-cyan-700/50 flex items-center justify-center">
              <Bot className="w-4 h-4 animate-spin" />
            </div>
            <div className="bg-[#15223F] p-3 rounded-xl border border-[#22355A] flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce"></span>
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.2s]"></span>
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.4s]"></span>
              <span className="text-slate-300 ml-1">Searching local knowledge base...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Bar */}
      <div className="px-5 py-2.5 bg-[#0C1428] border-t border-[#1C2C4E] flex items-center space-x-2 overflow-x-auto no-scrollbar">
        <span className="text-[11px] font-semibold text-slate-400 shrink-0">Quick Queries:</span>
        {quickPrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(p.query)}
            disabled={isLoading}
            className="text-xs shrink-0 bg-[#14203D] hover:bg-[#1E2E54] text-slate-300 hover:text-white px-2.5 py-1 rounded-full border border-slate-700/60 transition-colors"
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div className="p-4 bg-[#101B34] border-t border-[#1E2E4E]">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center space-x-3"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about flights (AI-204), gate directions, baggage claim, lounges..."
            className="flex-1 bg-[#090F20] text-slate-100 placeholder-slate-500 text-sm px-4 py-3 rounded-xl border border-slate-700/80 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white p-3 rounded-xl shadow-md shadow-cyan-500/20 disabled:opacity-40 transition-all shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
