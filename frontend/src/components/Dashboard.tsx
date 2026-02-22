"use client";

import React, { useEffect, useState, useRef } from 'react';
import dynamic from 'next/dynamic';
import { useAtom } from 'jotai';
import { vitalsAtom, agentStatesAtom, messagesAtom, isConnectedAtom } from '@/lib/store';
import { Activity, Heart, Moon, Zap, AlertTriangle, MessageSquare, Shield, Settings, Menu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ChatPanel from './ChatPanel';
import AgentActivity from './AgentActivity';

const MindMap3D = dynamic(() => import('./MindMap3D'), {
    ssr: false,
    loading: () => (
        <div className="w-full h-full flex items-center justify-center">
            <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 border-2 border-[#4ecdc4]/40 border-t-[#4ecdc4] rounded-full animate-spin" />
                <p className="text-[#4ecdc4]/60 font-orbitron text-xs tracking-widest uppercase">Initializing Mesh...</p>
            </div>
        </div>
    )
});

const AGENTS_CONFIG = [
    { id: "orchestrator", name: "Orchestrator", color: "#4ecdc4", size: 64, desc: "Command Hub" },
    { id: "vitals_agent", name: "Vitals", color: "#ff6b6b", size: 48, desc: "Biometrics" },
    { id: "counselor_agent", name: "Counselor", color: "#aa6dc9", size: 48, desc: "Mental Support" },
    { id: "exercise_agent", name: "Exercise", color: "#feca57", size: 48, desc: "Fitness" },
    { id: "sleep_agent", name: "Sleep", color: "#54a0ff", size: 48, desc: "Rest Cycles" },
    { id: "nutrition_agent", name: "Nutrition", color: "#5f27cd", size: 48, desc: "Sustenance" },
    { id: "mood_agent", name: "Mood", color: "#ff9f43", size: 44, desc: "Emotions" },
    { id: "social_agent", name: "Social", color: "#ee5253", size: 44, desc: "Crew" },
    { id: "alert_agent", name: "Alert", color: "#ff4757", size: 44, desc: "Emergency" },
    { id: "digital_twin", name: "Digital Twin", color: "#7bed9f", size: 44, desc: "Prediction" },
];

export default function Dashboard() {
    const [vitals, setVitals] = useAtom(vitalsAtom);
    const [agentStates, setAgentStates] = useAtom(agentStatesAtom);
    const [messages, setMessages] = useAtom(messagesAtom);
    const [isConnected, setIsConnected] = useAtom(isConnectedAtom);
    const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
    const [mounted, setMounted] = useState(false);
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        setMounted(true);
    }, []);

    useEffect(() => {
        const connectWebSocket = () => {
            const socket = new WebSocket('ws://localhost:8000/ws');
            socketRef.current = socket;

            socket.onopen = () => {
                console.log('Connected to MAITRI Backend');
                setIsConnected(true);
            };

            socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'connected') {
                        console.log('WS Connected:', data.message);
                        setIsConnected(true);
                    } else if (data.type === 'vitals_update') {
                        const vitalsData = data.data?.vitals;
                        if (vitalsData) {
                            setVitals(vitalsData);
                        }
                    } else if (data.type === 'agent_status') {
                        const agentsData = data.data?.agents;
                        if (agentsData) {
                            const formatted: Record<string, any> = {};
                            Object.entries(agentsData).forEach(([key, val]: [string, any]) => {
                                formatted[key] = {
                                    name: val.name,
                                    type: val.type,
                                    state: val.state,
                                    status_message: val.status_message,
                                    status: val.state === 'processing' ? 'Processing' : val.state === 'alert' ? 'Alert' : 'Active',
                                };
                            });
                            setAgentStates(formatted);
                        }
                    } else if (data.type === 'chat_response') {
                        const response = data.data?.response;
                        if (response) {
                            setMessages(prev => [...prev, {
                                role: 'ai',
                                text: typeof response === 'string' ? response : response.response || JSON.stringify(response),
                                timestamp: new Date().toLocaleTimeString(),
                            }]);
                        }
                    }
                } catch (err) {
                    console.error('WS parse error:', err);
                }
            };

            socket.onclose = () => {
                console.log('Disconnected from MAITRI Backend');
                setIsConnected(false);
                setTimeout(connectWebSocket, 3000);
            };

            socket.onerror = (err) => {
                console.log('WS Error - attempting to reconnect...');
            };
        };

        connectWebSocket();

        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    }, [setVitals, setAgentStates, setMessages, setIsConnected]);

    const sendChatMessage = async (text: string) => {
        setMessages(prev => [...prev, { role: 'user', text, timestamp: new Date().toLocaleTimeString() }]);

        if (socketRef.current?.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify({ type: 'chat', text }));
        } else {
            try {
                const response = await fetch('http://localhost:8000/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text }),
                });
                const data = await response.json();
                setMessages(prev => [...prev, { 
                    role: 'ai', 
                    text: data.response || data.error || 'No response', 
                    timestamp: new Date().toLocaleTimeString() 
                }]);
            } catch (err) {
                setMessages(prev => [...prev, { 
                    role: 'ai', 
                    text: 'Connection error. Please check if backend is running.', 
                    timestamp: new Date().toLocaleTimeString() 
                }]);
            }
        }
    };

    return (
        <div className="flex flex-col h-screen bg-[#0a0f1f] text-white p-4 gap-4 overflow-hidden relative">
            <div className="nebula-bg" />

            <header className="flex justify-between items-center glass p-4 h-20 shrink-0">
                <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all ${isConnected ? 'bg-[#4ecdc4]/20 border-[#4ecdc4]/40 animate-pulse' : 'bg-red-500/20 border-red-500/40'}`}>
                        <Zap className={isConnected ? 'text-[#4ecdc4]' : 'text-red-500'} />
                    </div>
                    <div>
                        <h1 className="font-orbitron text-xl font-bold tracking-widest text-glow-primary">MAITRI</h1>
                        <p className="text-xs text-[#4ecdc4]/60 uppercase tracking-tighter">Mission: Astronaut Well-Being</p>
                    </div>
                </div>

                <div className="flex gap-6 items-center">
                    <div className="text-right">
                        <p className="text-xs text-white/40 uppercase">Mission Clock</p>
                        <p className="font-mono text-2xl text-[#4ecdc4]">{mounted && vitals.heart_rate ? `245:12:${String(45 + Math.floor(Math.random() * 15)).padStart(2, '0')}:${String(10 + Math.floor(Math.random() * 50)).padStart(2, '0')}` : '---:--:--:--'}</p>
                    </div>

                    <div className="h-10 w-px bg-white/10" />

                    <div className="flex flex-col items-center">
                        <div className="flex gap-1">
                            {[1, 2, 3, 4, 5].map((i) => (
                                <div key={i} className={`h-1 w-4 rounded-full ${i <= 4 ? 'bg-[#4ecdc4]' : 'bg-[#4ecdc4]/20'}`} />
                            ))}
                        </div>
                        <p className="text-[10px] text-[#4ecdc4]/60 mt-1">AI TRUST: {isConnected ? '92%' : 'OFFLINE'}</p>
                    </div>

                    <button className="flex items-center gap-2 bg-red-500/20 text-red-500 border border-red-500/40 px-4 py-2 rounded-lg hover:bg-red-500/30 transition-all active:scale-95 group">
                        <AlertTriangle className="group-hover:animate-bounce" size={18} />
                        <span className="font-bold text-sm">EMERGENCY</span>
                    </button>
                </div>
            </header>

            <div className="flex flex-1 gap-4 min-h-0">
                <aside className="w-80 glass flex flex-col p-4 gap-4 shrink-0">
                    <div className="aspect-square glass-dark rounded-xl relative overflow-hidden flex items-center justify-center border border-white/10">
                        <div className="text-center p-6">
                            <div className="w-32 h-32 rounded-full border-2 border-[#4ecdc4]/40 p-1 mb-4 mx-auto relative cursor-pointer">
                                <div className="w-full h-full rounded-full bg-gradient-to-br from-[#4ecdc4]/20 to-[#aa6dc9]/20 flex items-center justify-center">
                                    <Shield className="text-[#4ecdc4] w-12 h-12" />
                                </div>
                                <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-[#4ecdc4] text-[#0a0f1f] text-[10px] font-bold px-2 py-0.5 rounded-full">
                                    {isConnected ? 'ONLINE' : 'OFFLINE'}
                                </div>
                            </div>
                            <h3 className="font-orbitron font-bold text-[#4ecdc4]">MAITRI AI</h3>
                            <p className="text-xs text-white/60 mb-4 italic">Monitoring your status, Commander.</p>
                            <div className="flex justify-center gap-1 h-8 items-center">
                                {[1, 2, 3, 4, 5, 2, 1, 3, 4, 3, 2].map((h, i) => (
                                    <motion.div
                                        key={i}
                                        animate={{ height: [`${h * 10}%`, `${h * 20}%`, `${h * 10}%`] }}
                                        transition={{ repeat: Infinity, duration: 0.5, delay: i * 0.05 }}
                                        className="w-1 bg-[#4ecdc4]/40 rounded-full"
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="glass-dark p-4 rounded-xl">
                        <h4 className="text-xs text-white/40 uppercase font-bold mb-3">Vitals</h4>
                        <div className="grid grid-cols-2 gap-3">
                            <div className="glass p-3 rounded-lg">
                                <Heart className="text-red-500 mb-1" size={16} />
                                <p className="text-lg font-mono">{vitals.heart_rate || '--'}</p>
                                <p className="text-[10px] text-white/40">BPM</p>
                            </div>
                            <div className="glass p-3 rounded-lg">
                                <Activity className="text-blue-500 mb-1" size={16} />
                                <p className="text-lg font-mono">{vitals.o2_level || '--'}%</p>
                                <p className="text-[10px] text-white/40">O₂</p>
                            </div>
                            <div className="glass p-3 rounded-lg">
                                <Moon className="text-purple-500 mb-1" size={16} />
                                <p className="text-lg font-mono">{vitals.sleep_quality || '--'}%</p>
                                <p className="text-[10px] text-white/40">Sleep</p>
                            </div>
                            <div className="glass p-3 rounded-lg">
                                <Zap className="text-yellow-500 mb-1" size={16} />
                                <p className="text-lg font-mono">{vitals.stress_level || '--'}</p>
                                <p className="text-[10px] text-white/40">Stress</p>
                            </div>
                        </div>
                    </div>

                    <button onClick={() => sendChatMessage("I'm feeling stressed")} className="glass-card p-3 text-left text-sm font-medium hover:text-[#4ecdc4] flex justify-between items-center group">
                        Feeling Stressed
                        <Zap size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <button onClick={() => sendChatMessage("I need exercise")} className="glass-card p-3 text-left text-sm font-medium hover:text-[#4ecdc4] flex justify-between items-center group">
                        Need Exercise
                        <Zap size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <button onClick={() => sendChatMessage("How's my health?")} className="glass-card p-3 text-left text-sm font-medium hover:text-[#4ecdc4] flex justify-between items-center group">
                        Health Summary
                        <Zap size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                </aside>

                <main className="flex-1 glass relative overflow-hidden">
                    <div className="absolute top-4 left-4 z-10">
                        <h2 className="font-orbitron text-sm text-[#4ecdc4]/80 flex items-center gap-2">
                            <Activity size={16} /> AGENTIC ORCHESTRATION MESH
                        </h2>
                    </div>
                    <div className="w-full h-full">
                        <MindMap3D agents={AGENTS_CONFIG} agentStates={agentStates} />
                    </div>

                    <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end">
                        <div className="glass-dark p-4 rounded-xl border border-white/10 flex flex-col gap-3">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-[#4ecdc4]/20 flex items-center justify-center border border-[#4ecdc4]/40">
                                    <Shield size={20} className="text-[#4ecdc4]" />
                                </div>
                                <div>
                                    <p className="text-[10px] text-white/40 uppercase">Active Agent</p>
                                    <p className="text-sm font-bold text-[#4ecdc4]">{selectedAgent || 'ORCHESTRATOR'}</p>
                                </div>
                            </div>
                            <div className="text-[10px] text-white/60 max-w-[200px]">
                                Managing {AGENTS_CONFIG.length} specialized agents. System {isConnected ? 'operational' : 'connecting...'}.
                            </div>
                        </div>

                        <div className="flex gap-2">
                            <div className="glass-dark p-3 rounded-lg border border-white/10 flex items-center gap-3">
                                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                                <span className="text-[10px] uppercase font-bold">{isConnected ? 'Link Stable' : 'Disconnected'}</span>
                            </div>
                            <div className="glass-dark p-3 rounded-lg border border-white/10 flex items-center gap-3">
                                <span className="text-[10px] uppercase font-bold text-white/40">Latency</span>
                                <span className="text-[10px] font-mono">{isConnected ? '14ms' : '--'}</span>
                            </div>
                        </div>
                    </div>
                </main>

                <aside className="w-96 flex flex-col gap-4 shrink-0">
                    <div className="flex-1 glass overflow-hidden flex flex-col p-4">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-orbitron text-sm flex items-center gap-2">
                                <Menu size={16} className="text-[#4ecdc4]" /> AGENT STATUS
                            </h3>
                            <span className="text-[10px] bg-[#4ecdc4]/20 text-[#4ecdc4] px-2 py-0.5 rounded">{AGENTS_CONFIG.length} ACTIVE</span>
                        </div>
                        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
                            <AgentActivity agents={AGENTS_CONFIG} agentStates={agentStates} />
                        </div>
                    </div>

                    <div className="h-80 glass flex flex-col overflow-hidden">
                        <div className="flex items-center gap-2 p-4 pb-0">
                            <MessageSquare size={16} className="text-[#4ecdc4]" />
                            <h3 className="font-orbitron text-sm">MAITRI CHAT</h3>
                        </div>
                        <ChatPanel onSendMessage={sendChatMessage} />
                    </div>
                </aside>
            </div>

            <footer className="h-20 glass shrink-0 flex items-center px-6 gap-8 overflow-hidden">
                <div className="flex gap-8 items-center">
                    <div className="flex flex-col gap-1">
                        <span className="text-[10px] text-white/40 font-bold">OXYGEN</span>
                        <div className="flex items-center gap-3">
                            <span className="font-mono text-lg">{vitals.o2_level?.toFixed(1) || '21.0'}%</span>
                            <div className="w-12 h-6 glass-dark rounded relative">
                                <div className="absolute inset-y-0 left-0 bg-blue-500/50 w-[80%] rounded-l" />
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col gap-1">
                        <span className="text-[10px] text-white/40 font-bold">CABIN TEMP</span>
                        <div className="flex items-center gap-3">
                            <span className="font-mono text-lg">{vitals.temperature?.toFixed(1) || '22.0'}°C</span>
                            <div className="w-12 h-6 glass-dark rounded relative">
                                <div className="absolute inset-y-0 left-0 bg-orange-500/50 w-[65%] rounded-l" />
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col gap-1">
                        <span className="text-[10px] text-white/40 font-bold">CO₂</span>
                        <div className="flex items-center gap-3">
                            <span className="font-mono text-lg">{(vitals.co2_level || 0.04).toFixed(2)}%</span>
                            <div className="w-12 h-6 glass-dark rounded relative">
                                <div className="absolute inset-y-0 left-0 bg-green-500/50 w-[30%] rounded-l" />
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex-1 flex flex-col gap-1">
                    <div className="flex justify-between text-[10px] text-white/40 uppercase font-bold">
                        <span>Timeline: Phase 4 Implementation</span>
                        <span>T-Minus 12h 45m</span>
                    </div>
                    <div className="h-2 glass-dark rounded-full overflow-hidden relative">
                        <motion.div
                            animate={{ x: ["-100%", "100%"] }}
                            transition={{ repeat: Infinity, duration: 3, ease: "linear" }}
                            className="absolute inset-y-0 w-20 bg-[#4ecdc4]/20 blur-sm"
                        />
                        <div className="absolute inset-y-0 left-0 bg-[#4ecdc4] w-[75%] rounded-full shadow-[0_0_10px_rgba(78,205,196,0.5)]" />
                    </div>
                </div>

                <div className="flex gap-4 items-center">
                    <div className="flex flex-col items-end">
                        <p className="text-[10px] text-white/40 uppercase">Earth Link</p>
                        <p className="text-xs font-bold text-green-500">{isConnected ? 'CONNECTED' : 'OFFLINE'}</p>
                    </div>
                    <div className="w-10 h-10 rounded-full border-2 border-[#4ecdc4]/20 flex items-center justify-center">
                        <Activity size={18} className={`text-[#4ecdc4] ${isConnected ? 'animate-pulse' : ''}`} />
                    </div>
                </div>
            </footer>
        </div>
    );
}
