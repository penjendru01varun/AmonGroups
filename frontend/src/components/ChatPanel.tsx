"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useAtom } from 'jotai';
import { messagesAtom } from '@/lib/store';
import { Send, User, Bot, Mic, Volume2, ThumbsUp, ThumbsDown, Sparkles, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { ChatMessage } from '@/types';

interface ChatPanelProps {
    onSendMessage?: (text: string) => void;
}

const KNOWLEDGE_BASE = {
  greeting: ["hello", "hi", "hey", "greetings", "good morning", "good evening"],
  
  about: {
    keywords: ["what is maitri", "about", "who are you", "introduce", "tell me about"],
    response: `**Orchestrator here:** MAITRI (Mental & physical AI Assistant for astronauts) is a multi-agent AI system designed to monitor and support astronaut well-being during space missions.

We use **10 specialized AI agents** that work together to track physical health, provide psychological support, manage mission tasks, and predict potential issues before they become critical.

**Our Capabilities:**
- ❤️ Real-time vitals monitoring
- 🧠 Psychological counseling with CBT
- 💪 Personalized exercise planning
- 😴 Sleep quality analysis
- 🍎 Nutrition tracking
- ⚡ Emergency detection
- 🔮 Predictive simulations

How can I help you today?`
  },
  
  agents: {
    keywords: ["agents", "what agents", "list agents", "who are the agents", "specialized agents"],
    response: `**Orchestrator here:** We have 10 specialized agents working together:

**Physical Cluster:**
- ❤️ **Vitals Monitor** - Tracks heart rate, O2, CO2, temperature
- 💪 **Exercise Coach** - Personalized microgravity workouts  
- 😴 **Sleep Analyst** - Sleep cycle analysis & optimization
- 🍎 **Nutrition Agent** - Meal planning & inventory

**Psychological Cluster:**
- 🧠 **Counselor Agent** - CBT-based emotional support
- 😊 **Mood Detector** - Emotion detection from text & vitals
- 👥 **Social Agent** - Crew morale & communication

**Intelligence Cluster:**
- ⚡ **Alert Agent** - Emergency detection & protocols
- 🔮 **Digital Twin** - Predictive simulations
- 🎯 **Orchestrator** - Task coordination (that's me!)

Which agent would you like to learn more about?`
  },
  
  vitals: {
    keywords: ["heart rate", "vitals", "health", "oxygen", "o2", "temperature", "breathing"],
    response: (vitals: any) => `**Vitals Monitor here:** Current readings:
- ❤️ Heart Rate: **${vitals?.heart_rate || 72} bpm** ${vitals?.heart_rate > 100 ? '(elevated)' : '(normal)'}
- 🫁 O2 Saturation: **${vitals?.o2_level || 98}%** ${vitals?.o2_level < 95 ? '(low - rest recommended)' : '(optimal)'}
- 🌡️ Temperature: **${vitals?.temperature || 22}°C** (normal)
- 💨 CO2: **${vitals?.co2_level || 0.04}%** (normal)

All readings within acceptable parameters. Would you like me to explain any of these in more detail?`
  },
  
  anxious: {
    keywords: ["anxious", "stress", "worried", "nervous", "panic", "scared", "fear", "feeling down", "sad", "depressed", "lonely", "alone"],
    response: `**Counselor Agent here:** I'm here for you. Let's check your vitals... I see your heart rate is slightly elevated, which is a natural response to stress.

**Try this grounding technique:**
Name 5 things you can see → 4 you can touch → 3 you can hear → 2 you can smell → 1 you can taste.

Or we could do the 4-7-8 breathing: Inhale 4s, hold 7s, exhale 8s.

Would you like me to:
1. Play some calming music?
2. Connect you with a crew member?
3. Schedule a session with the mission psychologist?`
  },
  
  exercise: {
    keywords: ["exercise", "workout", "fitness", "training", "work out", "cardio", "strength"],
    response: `**Exercise Coach here:** Ready to get moving! Here are your options:

**Today's Recommendations:**
- 🏃 **Morning Cardio** - 30 min cycle session (08:00)
- 💪 **Resistance Training** - ARED workout (14:00)  
- 🧘 **Evening Stretch** - 15 min flexibility (20:00)

In microgravity, we need **2+ hours daily** to prevent muscle atrophy and bone loss.

Would you like me to:
1. Generate a custom workout plan?
2. Show your exercise history?
3. Explain the best exercises for bone health?`
  },
  
  sleep: {
    keywords: ["sleep", "tired", "exhausted", "rest", "insomnia", "can't sleep", "bedtime", "night"],
    response: `**Sleep Analyst here:** Let me check your recent sleep data...

**Last 7 Days Average:**
- ⏰ Sleep Duration: 6.8 hours (target: 7-8)
- 😴 Sleep Efficiency: 82%
- 🌙 Deep Sleep: 22% (optimal: 20-25%)

**Recommendations:**
1. Maintain consistent bedtime (target: 22:30)
2. Reduce screen time 1 hour before sleep
3. Consider a 20-min afternoon nap

Would you like me to:
1. Show detailed sleep analysis?
2. Optimize your sleep schedule?
3. Set up a smart alarm?`
  },
  
  nutrition: {
    keywords: ["food", "eat", "nutrition", "hungry", "meal", "drink", "water", "calories"],
    response: `**Nutrition Agent here:** Here's your daily nutrition summary:

**Today's Intake:**
- 🍳 Breakfast: 380 cal (completed 07:00)
- 🍱 Lunch: 450 cal (completed 12:30)
- 🍝 Dinner: Pending (18:00)
- 🍿 Snacks: 170 cal

**Hydration:** 1,800ml / 2,500ml target (72%)

**Space Food Tip:** Did you know? All our meals are specially formulated to maintain bone density in microgravity!

Would you like me to:
1. Generate tomorrow's meal plan?
2. Check food inventory?
3. Track hydration more closely?`
  },
  
  emergency: {
    keywords: ["emergency", "help", "danger", "warning", "alert", "critical", "not breathing", "heart stopped"],
    response: `**Alert Agent here:** ⚠️ **EMERGENCY PROTOCOLS ACTIVE**

If this is a real emergency:
1. **STAY CALM** - Panic increases heart rate
2. **CHECK YOURSELF** - Are you conscious? Breathing?
3. **PRESS EMERGENCY BUTTON** on your console
4. **RADIO MISSION CONTROL** immediately

**Current Alert Status:** 🟢 All systems normal

For non-emergencies, I'm happy to help! What do you need?`
  },
  
  digital_twin: {
    keywords: ["predict", "future", "simulation", "what if", "digital twin", "forecast", "outcome"],
    response: `**Digital Twin here:** 🔮 I've analyzed your patterns...

**24-Hour Prediction:**
- Fatigue Peak: 68% at 16:00 UTC
- Best Performance Window: 10:00-14:00
- Recommended Rest: 20:00

**If you skip exercise today:**
- Muscle atrophy risk: +5%
- Energy levels tomorrow: -12%

**If you sleep extra 1 hour:**
- Cognitive performance: +15%
- Reaction time improvement: +8%

Would you like me to run a specific simulation?`
  },
  
  system_status: {
    keywords: ["status", "system", "how are you", "operational", "working", "performance"],
    response: (vitals: any) => `**Orchestrator here:** All systems operational! 🟢

**System Status:**
- ✅ Agents Active: 10/10
- ✅ WebSocket: Connected
- ✅ Response Time: 47ms avg
- ✅ Memory Usage: 42%
- ✅ CPU Load: 23%

**Your Vitals:**
- ❤️ HR: ${vitals?.heart_rate || 72} bpm
- 🫁 O2: ${vitals?.o2_level || 98}%
- 😴 Sleep: 82% quality
- ⚡ Stress: ${vitals?.stress_level || 25}% (low)

Everything looks healthy! What would you like to explore?`
  },
  
  help: {
    keywords: ["help", "commands", "what can you do", "how does this work", "guide", "tutorial"],
    response: `**Orchestrator here:** Here's what I can help you with:

**🗣️ Just Talk:**
- "I'm feeling anxious" → Counselor support
- "Show my vitals" → Health data
- "Generate workout" → Exercise plan

**📊 Ask About:**
- Any specific agent and their function
- Your health metrics and trends
- System status and performance

**🔧 Troubleshooting:**
- "Not responding" → Check connections
- "Vitals not updating" → Refresh page

**💡 Pro Tips:**
- Ask specific agents directly: "Vitals, show my heart rate"
- Ask "what if" scenarios: Digital Twin predictions
- Request explanations: "How does the counselor work?"

What would you like to explore?`
  }
};

const SUGGESTED_REPLIES: Record<string, string[]> = {
  greeting: ["Show my vitals", "What agents do you have?", "I'm feeling anxious", "Generate a workout"],
  vitals: ["Show detailed analysis", "Check for anomalies", "What do these numbers mean?"],
  anxious: ["Let's do breathing", "Play calming music", "I want to talk", "Connect me with someone"],
  exercise: ["Create workout plan", "Show exercise history", "Best exercises for bones"],
  sleep: ["Show sleep analysis", "Optimize my schedule", "Set up smart alarm"],
  nutrition: ["Generate meal plan", "Check inventory", "Track hydration"],
  digital_twin: ["Predict my fatigue", "What if I skip exercise?", "Best time for tasks?"],
  system_status: ["Show agent status", "Performance metrics", "Any active alerts?"],
  default: ["Show my vitals", "What agents do you have?", "Generate a workout", "How are you?"]
};

function detectIntent(text: string): string {
  const lower = text.toLowerCase();
  
  const greetings = KNOWLEDGE_BASE.greeting;
  if (greetings.some(g => lower.includes(g))) return 'greeting';
  
  if (lower.includes('anxious') || lower.includes('stress') || lower.includes('worried') || 
      lower.includes('nervous') || lower.includes('panic') || lower.includes('sad') ||
      lower.includes('depressed') || lower.includes('lonely') || lower.includes('alone') ||
      lower.includes('feeling down')) return 'anxious';
  
  if (lower.includes('vital') || lower.includes('heart') || lower.includes('oxygen') || 
      lower.includes('o2') || lower.includes('temperature') || lower.includes('breath')) return 'vitals';
  
  if (lower.includes('exercise') || lower.includes('workout') || lower.includes('fitness') ||
      lower.includes('training') || lower.includes('cardio') || lower.includes('strength')) return 'exercise';
  
  if (lower.includes('sleep') || lower.includes('tired') || lower.includes('exhausted') ||
      lower.includes('rest') || lower.includes('insomnia') || lower.includes('bedtime')) return 'sleep';
  
  if (lower.includes('food') || lower.includes('eat') || lower.includes('nutrition') ||
      lower.includes('hungry') || lower.includes('meal') || lower.includes('water') || lower.includes('drink')) return 'nutrition';
  
  if (lower.includes('predict') || lower.includes('future') || lower.includes('simulation') ||
      lower.includes('what if') || lower.includes('digital twin') || lower.includes('forecast')) return 'digital_twin';
  
  if (lower.includes('emergency') || lower.includes('danger') || lower.includes('alert') ||
      lower.includes('critical') || lower.includes('warning')) return 'emergency';
  
  if (lower.includes('status') || lower.includes('system') || lower.includes('working') ||
      lower.includes('operational') || lower.includes('performance') || lower.includes('how are you')) return 'system_status';
  
  if (lower.includes('agent') || lower.includes('what can you do')) return 'agents';
  
  if (lower.includes('about') || lower.includes('who are you') || lower.includes('maitri')) return 'about';
  
  if (lower.includes('help') || lower.includes('how does') || lower.includes('guide') ||
      lower.includes('tutorial') || lower.includes('commands')) return 'help';
  
  return 'default';
}

export default function ChatPanel({ onSendMessage }: ChatPanelProps) {
  const [messages, setMessages] = useAtom(messagesAtom);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [suggestedReplies, setSuggestedReplies] = useState<string[]>(SUGGESTED_REPLIES.default);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [ratings, setRatings] = useState<Record<number, 'up' | 'down'>>({});
  const [vitals, setVitals] = useState<any>(null);

  useEffect(() => {
    const fetchVitals = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/vitals');
        const data = await res.json();
        setVitals(data?.vitals);
      } catch (e) {
        console.log('Could not fetch vitals');
      }
    };
    fetchVitals();
    const interval = setInterval(fetchVitals, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const generateResponse = (userText: string): string => {
    const intent = detectIntent(userText);
    const knowledge = KNOWLEDGE_BASE[intent as keyof typeof KNOWLEDGE_BASE];
    
    if (!knowledge || typeof knowledge === 'string') {
      return knowledge || `**Orchestrator here:** I understand you're asking about "${userText}". Could you rephrase that? I'm optimized for questions about:
- Your vitals and health
- Exercise and sleep
- Nutrition and meals  
- Agent capabilities
- System status`;
    }
    
    if (typeof knowledge.response === 'function') {
      return knowledge.response(vitals);
    }
    
    return knowledge.response;
  };

  const handleSend = () => {
    if (!input.trim()) return;
    
    const userMsg: ChatMessage = { role: 'user', text: input, timestamp: new Date().toLocaleTimeString() };
    setMessages((prev: ChatMessage[]) => [...prev, userMsg]);
    setShowSuggestions(false);
    
    if (onSendMessage) {
      onSendMessage(input);
    }
    
    setIsTyping(true);
    
    setTimeout(() => {
      const response = generateResponse(input);
      setMessages((prev: ChatMessage[]) => [...prev, { 
        role: 'ai', 
        text: response, 
        timestamp: new Date().toLocaleTimeString(),
      }]);
      setIsTyping(false);
      setShowSuggestions(true);
      setSuggestedReplies(SUGGESTED_REPLIES[intent as string] || SUGGESTED_REPLIES.default);
    }, 800 + Math.random() * 700);
    
    setInput('');
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  const handleRate = (index: number, rating: 'up' | 'down') => {
    setRatings(prev => ({ ...prev, [index]: rating }));
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 custom-scrollbar" ref={scrollRef}>
        {messages.length === 0 && !isTyping && (
          <div className="text-center py-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-[#4ecdc4] to-[#aa6dc9] flex items-center justify-center"
            >
              <Sparkles className="text-white" size={32} />
            </motion.div>
            <p className="text-[10px] uppercase font-orbitron text-[#4ecdc4] mb-2">MAITRI AI Assistant</p>
            <p className="text-[10px] text-white/60 mt-2 px-4">
              Hi! I'm here to help with any questions about your health, the agents, or the system. 
              Try asking about your vitals, exercise, sleep, or just say hi! 👋
            </p>
          </div>
        )}
        
        <AnimatePresence initial={false}>
          {messages.map((msg: ChatMessage, i: number) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[90%] p-3 rounded-2xl flex gap-3 ${msg.role === 'user' ? 'bg-[#4ecdc4]/20 border border-[#4ecdc4]/30' : 'bg-white/5 border border-white/10'}`}>
                {msg.role === 'ai' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#4ecdc4] to-[#aa6dc9] flex items-center justify-center shrink-0">
                    <Bot size={16} className="text-white" />
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-mono text-white/40 mb-1">{msg.role === 'user' ? 'COMMANDER' : 'MAITRI'}</p>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  <p className="text-[10px] text-white/20 mt-1 text-right">{msg.timestamp}</p>
                  
                  {msg.role === 'ai' && (
                    <div className="flex items-center gap-2 mt-2 pt-2 border-t border-white/10">
                      <button 
                        onClick={() => handleRate(i, 'up')}
                        className={`p-1 rounded ${ratings[i] === 'up' ? 'text-green-500' : 'text-white/30 hover:text-white/60'}`}
                      >
                        <ThumbsUp size={12} />
                      </button>
                      <button 
                        onClick={() => handleRate(i, 'down')}
                        className={`p-1 rounded ${ratings[i] === 'down' ? 'text-red-500' : 'text-white/30 hover:text-white/60'}`}
                      >
                        <ThumbsDown size={12} />
                      </button>
                    </div>
                  )}
                </div>
                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-[#aa6dc9]/30 flex items-center justify-center shrink-0">
                    <User size={16} className="text-[#aa6dc9]" />
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isTyping && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="flex items-center gap-3 p-3 rounded-2xl bg-white/5 border border-white/10">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#4ecdc4] to-[#aa6dc9] flex items-center justify-center">
                <Bot size={16} className="text-white" />
              </div>
              <div className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    animate={{ scale: [0.8, 1.2, 0.8] }}
                    transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.15 }}
                    className="w-2 h-2 rounded-full bg-[#4ecdc4]"
                  />
                ))}
              </div>
              <span className="text-xs text-white/40">Analyzing...</span>
            </div>
          </motion.div>
        )}
      </div>

      {showSuggestions && suggestedReplies.length > 0 && messages.length < 3 && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="px-4 pb-2"
        >
          <div className="flex flex-wrap gap-2">
            {suggestedReplies.map((reply, i) => (
              <button
                key={i}
                onClick={() => handleSuggestionClick(reply)}
                className="text-[10px] bg-white/5 hover:bg-[#4ecdc4]/20 hover:border-[#4ecdc4]/40 px-3 py-1.5 rounded-full border border-white/10 text-white/70 transition-all"
              >
                {reply}
              </button>
            ))}
          </div>
        </motion.div>
      )}

      <div className="p-4 bg-black/20 border-t border-white/5">
        <div className="relative flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask MAITRI anything..."
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-[#4ecdc4]/50 transition-all text-white placeholder-white/30"
          />
          <button
            onClick={handleSend}
            className="p-3 bg-[#4ecdc4]/20 hover:bg-[#4ecdc4]/30 border border-[#4ecdc4]/40 rounded-xl text-[#4ecdc4] transition-all"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
