export interface Vitals {
    heart_rate: number;
    o2_saturation?: number;
    sleep_quality?: number;
    stress_level?: number;
    o2_level?: number;
    co2_level?: number;
    temperature?: number;
    hr_variability?: number;
    timestamp?: string;
}

export interface AgentStatus {
    name: string;
    type: string;
    state: string;
    status_message: string;
    capabilities: string[];
    metrics?: {
        tasks_processed: number;
        avg_response_time: number;
        error_rate: number;
    };
}

export interface ChatMessage {
    role: 'user' | 'ai';
    text: string;
    timestamp: string;
    emotion?: string;
}

export interface Alert {
    id: string;
    type: string;
    severity: number;
    severity_name: string;
    message: string;
    source: string;
    created_at: string;
    acknowledged: boolean;
    resolved: boolean;
}

export interface Agent {
    agent_id: string;
    name: string;
    type: string;
    state: string;
    status_message: string;
    capabilities: string[];
}

export interface Workout {
    id: string;
    type: string;
    intensity: string;
    estimated_duration: number;
    warmup: Array<{name: string; duration: number; sets: number}>;
    main_exercises: Array<{name: string; duration: number; sets: number; form_cues: string[]}>;
    cooldown: Array<{name: string; duration: number; sets: number}>;
    calories_burned_estimate: number;
    bone_density_impact: string;
}

export interface MealPlan {
    date: string;
    meals: {
        breakfast: {name: string; calories: number; protein: number; carbs: number};
        lunch: {name: string; calories: number; protein: number; carbs: number};
        dinner: {name: string; calories: number; protein: number; carbs: number};
        snacks: {name: string; calories: number; protein: number; carbs: number};
    };
    total_calories: number;
    total_protein: number;
    total_carbs: number;
}
