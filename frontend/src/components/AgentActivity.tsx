"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Activity } from 'lucide-react';

interface AgentConfig {
    id: string;
    name: string;
    color: string;
    size: number;
    desc: string;
}

interface AgentStates {
    [key: string]: {
        name?: string;
        type?: string;
        state?: string;
        status_message?: string;
        status?: string;
    };
}

interface AgentActivityProps {
    agents: AgentConfig[];
    agentStates: AgentStates;
}

export default function AgentActivity({ agents, agentStates }: AgentActivityProps) {
    const getAgentState = (agentId: string) => {
        const state = agentStates[agentId];
        if (!state) return { status: 'idle', message: 'Monitoring...' };
        
        const status = state.status || state.state || 'idle';
        return {
            status: status === 'processing' ? 'Processing' : status === 'alert' ? 'Alert' : 'Active',
            message: state.status_message || state.state || 'Monitoring...',
        };
    };

    return (
        <div className="flex flex-col gap-2 p-2">
            {agents.map((agent, i) => {
                const agentState = getAgentState(agent.id);
                const isActive = agentState.status === 'Active';
                const isProcessing = agentState.status === 'Processing';
                const isAlert = agentState.status === 'Alert';
                
                return (
                    <motion.div
                        key={agent.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className="glass-dark p-3 rounded-lg border border-white/5 hover:border-[#4ecdc4]/30 transition-all cursor-pointer group"
                    >
                        <div className="flex justify-between items-start mb-1">
                            <div className="flex items-center gap-2">
                                <div className={`w-1.5 h-1.5 rounded-full ${
                                    isAlert ? 'bg-red-500 animate-ping' :
                                    isProcessing ? 'bg-yellow-500 animate-pulse' :
                                    'bg-green-500'
                                }`} />
                                <span 
                                    className="text-xs font-bold font-orbitron group-hover:text-[#4ecdc4] transition-colors uppercase tracking-wider"
                                    style={{ color: isAlert ? '#ff4757' : isProcessing ? '#feca57' : agent.color }}
                                >
                                    {agent.name}
                                </span>
                            </div>
                            <Shield size={10} className="text-white/20" />
                        </div>
                        <p className="text-[10px] text-white/50 truncate">{agent.desc}</p>
                        <p className="text-[9px] text-white/30 mt-1">{agentState.message}</p>

                        {isProcessing && (
                            <div className="mt-2 w-full bg-white/5 h-0.5 rounded-full overflow-hidden">
                                <motion.div
                                    animate={{ x: ["-100%", "100%"] }}
                                    transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                                    className="h-full w-full bg-[#4ecdc4]/40"
                                />
                            </div>
                        )}
                    </motion.div>
                );
            })}
        </div>
    );
}
