export interface QuestInfo {
  active: string[];
  completed: string[];
  done: boolean;
}

export interface StateSnapshot {
  location_id: string;
  location_name: string;
  location_description: string;
  inventory: string[];
  quests: Record<string, QuestInfo>;
  turn_number: number;
}

export interface SessionResponse {
  session_id: string;
  state: StateSnapshot;
}

export interface TurnResponse {
  success: boolean;
  narration: string;
  state: StateSnapshot;
}

export interface LogEntry {
  id: number;
  input: string;
  narration: string;
  success: boolean;
}
