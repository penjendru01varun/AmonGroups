"use client";

import React, { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

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

interface MindMap3DProps {
    agents: AgentConfig[];
    agentStates?: AgentStates;
}

const RING_RADII = [0, 120, 220];

export default function MindMap3D({ agents, agentStates = {} }: MindMap3DProps) {
    const [hoveredAgent, setHoveredAgent] = useState<string | null>(null);
    const [time, setTime] = useState(0);
    const containerRef = useRef<HTMLDivElement>(null);
    const [dimensions, setDimensions] = useState({ w: 600, h: 500 });

    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                setDimensions({
                    w: containerRef.current.clientWidth,
                    h: containerRef.current.clientHeight,
                });
            }
        };

        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    useEffect(() => {
        const id = setInterval(() => setTime(t => t + 0.008), 16);
        return () => clearInterval(id);
    }, []);

    const cx = dimensions.w / 2;
    const cy = dimensions.h / 2;

    const ring1Agents = agents.slice(1, 6);
    const ring2Agents = agents.slice(6);

    return (
        <div ref={containerRef} className="relative w-full h-full overflow-hidden" style={{ background: 'transparent' }}>
            <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 1 }}>
                {[1, 2].map(ring => (
                    <circle
                        key={ring}
                        cx={cx} cy={cy}
                        r={RING_RADII[ring]}
                        fill="none"
                        stroke="rgba(78,205,196,0.08)"
                        strokeWidth="1"
                        strokeDasharray="4 8"
                    />
                ))}

                {ring1Agents.map((agent, i) => {
                    const speed = 0.3 + i * 0.07;
                    const angle = (i * 72 * Math.PI / 180) + time * speed;
                    const x = cx + Math.cos(angle) * RING_RADII[1];
                    const y = cy + Math.sin(angle) * RING_RADII[1];
                    const isHov = hoveredAgent === agent.id;
                    return (
                        <line key={agent.name}
                            x1={cx} y1={cy} x2={x} y2={y}
                            stroke={agent.color}
                            strokeOpacity={isHov ? 0.6 : 0.15}
                            strokeWidth={isHov ? 1.5 : 0.8}
                            strokeDasharray="3 6"
                        />
                    );
                })}

                {ring2Agents.map((agent, i) => {
                    const speed = 0.18 + i * 0.04;
                    const angle = (i * 90 * Math.PI / 180) + time * speed;
                    const x = cx + Math.cos(angle) * RING_RADII[2];
                    const y = cy + Math.sin(angle) * RING_RADII[2];
                    
                    const hubIdx = i % ring1Agents.length;
                    const hubSpeed = 0.3 + hubIdx * 0.07;
                    const hubAngle = (hubIdx * 72 * Math.PI / 180) + time * hubSpeed;
                    const hx = cx + Math.cos(hubAngle) * RING_RADII[1];
                    const hy = cy + Math.sin(hubAngle) * RING_RADII[1];
                    
                    return (
                        <line key={agent.name}
                            x1={hx} y1={hy} x2={x} y2={y}
                            stroke={agent.color}
                            strokeOpacity={0.1}
                            strokeWidth={0.6}
                            strokeDasharray="2 8"
                        />
                    );
                })}
            </svg>

            <motion.div
                className="absolute flex flex-col items-center justify-center cursor-pointer"
                style={{
                    left: cx, top: cy,
                    transform: 'translate(-50%, -50%)',
                    zIndex: 10,
                    width: 80, height: 80,
                }}
                animate={{ scale: [1, 1.05, 1], rotate: [0, 5, -5, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
            >
                <div style={{
                    width: 80, height: 80,
                    borderRadius: '50%',
                    background: 'radial-gradient(circle at 35% 35%, rgba(78,205,196,0.6), rgba(10,15,31,0.9))',
                    border: '2px solid rgba(78,205,196,0.5)',
                    boxShadow: '0 0 30px rgba(78,205,196,0.4), inset 0 0 20px rgba(78,205,196,0.1)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                    <span style={{ fontSize: 28 }}>🧑‍🚀</span>
                </div>
                <span style={{
                    fontSize: 9, color: '#4ecdc4', marginTop: 4,
                    fontFamily: 'Orbitron, monospace', letterSpacing: 2, textTransform: 'uppercase',
                    textShadow: '0 0 10px rgba(78,205,196,0.8)', whiteSpace: 'nowrap',
                }}>ASTRONAUT</span>
            </motion.div>

            {[...ring1Agents, ...ring2Agents].map((agent, i) => {
                const isRingOne = i < ring1Agents.length;
                const idx = isRingOne ? i : i - ring1Agents.length;
                const speed = isRingOne ? (0.3 + idx * 0.07) : (0.18 + idx * 0.04);
                const baseAngle = isRingOne ? (idx * 72 * Math.PI / 180) : (idx * 90 * Math.PI / 180);
                const liveAngle = baseAngle + time * speed;
                const x = cx + Math.cos(liveAngle) * RING_RADII[isRingOne ? 1 : 2];
                const y = cy + Math.sin(liveAngle) * RING_RADII[isRingOne ? 1 : 2];
                const isHov = hoveredAgent === agent.id;
                
                const agentState = agentStates[agent.id];
                const isProcessing = agentState?.status === 'Processing' || agentState?.state === 'processing';
                const isAlert = agentState?.status === 'Alert' || agentState?.state === 'alert';

                return (
                    <motion.div
                        key={agent.id}
                        className="absolute flex flex-col items-center cursor-pointer"
                        style={{
                            left: x, top: y,
                            transform: 'translate(-50%, -50%)',
                            zIndex: isHov ? 20 : 5,
                        }}
                        onMouseEnter={() => setHoveredAgent(agent.id)}
                        onMouseLeave={() => setHoveredAgent(null)}
                        animate={{ scale: isHov ? 1.3 : 1 }}
                        transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                    >
                        {(isProcessing || isAlert) && (
                            <motion.div
                                className="absolute rounded-full"
                                style={{
                                    width: agent.size + 16, height: agent.size + 16,
                                    border: `1.5px solid ${isAlert ? '#ff4757' : agent.color}`,
                                    top: '50%', left: '50%',
                                    transform: 'translate(-50%, -50%)',
                                }}
                                animate={{ scale: [1, 1.5, 1], opacity: [0.7, 0, 0.7] }}
                                transition={{ duration: 1.5, repeat: Infinity }}
                            />
                        )}

                        <div style={{
                            width: agent.size, height: agent.size,
                            borderRadius: '50%',
                            background: `radial-gradient(circle at 35% 35%, ${agent.color}99, ${agent.color}22)`,
                            border: `1.5px solid ${agent.color}${isHov ? 'ff' : '66'}`,
                            boxShadow: isHov
                                ? `0 0 20px ${agent.color}99, 0 0 40px ${agent.color}44`
                                : `0 0 8px ${agent.color}44`,
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            transition: 'box-shadow 0.3s',
                        }}>
                            <span style={{
                                fontSize: 9, color: 'white', fontWeight: 700,
                                fontFamily: 'Orbitron, monospace', textAlign: 'center',
                                letterSpacing: 0.5, textShadow: `0 0 8px ${agent.color}`,
                                padding: '0 2px',
                            }}>
                                {agent.name.slice(0, 4).toUpperCase()}
                            </span>
                        </div>

                        <AnimatePresence>
                            {isHov && (
                                <motion.div
                                    initial={{ opacity: 0, y: -5, scale: 0.9 }}
                                    animate={{ opacity: 1, y: -8, scale: 1 }}
                                    exit={{ opacity: 0, y: -5, scale: 0.9 }}
                                    style={{
                                        position: 'absolute', bottom: '110%',
                                        background: 'rgba(10,15,31,0.95)',
                                        border: `1px solid ${agent.color}66`,
                                        borderRadius: 8, padding: '6px 10px',
                                        whiteSpace: 'nowrap', zIndex: 30,
                                        boxShadow: `0 4px 20px ${agent.color}33`,
                                    }}
                                >
                                    <p style={{ color: agent.color, fontSize: 10, fontFamily: 'Orbitron, monospace', fontWeight: 700 }}>
                                        {agent.name}
                                    </p>
                                    <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 9, marginTop: 2 }}>{agent.desc}</p>
                                    {agentState && (
                                        <p style={{ 
                                            color: isAlert ? '#ff4757' : isProcessing ? '#feca57' : '#4ecdc4', 
                                            fontSize: 8, marginTop: 2 
                                        }}>
                                            ● {agentState.status || agentState.state || 'Active'}
                                        </p>
                                    )}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </motion.div>
                );
            })}

            <div className="absolute top-4 left-4" style={{ zIndex: 25 }}>
                <p style={{
                    fontSize: 9, color: 'rgba(78,205,196,0.5)',
                    fontFamily: 'Orbitron, monospace', letterSpacing: 3,
                    textTransform: 'uppercase',
                }}>
                    ◎ Live Agentic Mesh — {agents.length} Nodes
                </p>
            </div>
        </div>
    );
}
