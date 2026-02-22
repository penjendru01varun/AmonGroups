"use client";
import { atom } from 'jotai';
import type { Vitals, AgentStatus, ChatMessage } from '@/types';

export const vitalsAtom = atom<Vitals>({
    heart_rate: 72,
    sleep_quality: 88,
    stress_level: 25,
    o2_level: 21,
    co2_level: 0.04,
    temperature: 22,
});

export const agentStatesAtom = atom<Record<string, AgentStatus>>({});

export const activeAgentAtom = atom<string | null>(null);

export const messagesAtom = atom<ChatMessage[]>([]);

export const missionEndClockAtom = atom<string>("245:12:45");

export const isConnectedAtom = atom<boolean>(false);
