export type TaskStatus =
  | "draft"
  | "scheduled"
  | "due"
  | "contacted"
  | "awaiting_response"
  | "completed"
  | "snoozed"
  | "rescheduled"
  | "cancelled"
  | "failed";

export type Task = {
  id: string;
  title: string;
  description?: string;

  status: TaskStatus;

  dueAt?: string;

  followUpEnabled: boolean;
  followUpAt?: string;

  retryEnabled: boolean;
  maxRetries?: number;
  retryIntervalMinutes?: number;

  createdAt: string;
  updatedAt: string;
};

export type NoteSource =
  | "written"
  | "digital_friend"
  | "system";

export type Note = {
  id: string;

  title: string;
  content: string;

  source: NoteSource;

  important: boolean;
  memory: boolean;

  createdAt: string;
  updatedAt: string;
};

export type Memory = {
  id: string;

  content: string;

  source:
    | "conversation"
    | "note"
    | "user_confirmed";

  confidence?: number;

  createdAt: string;
  updatedAt: string;
};

export type Guest = {
  id: string;

  name: string;
  email: string;
};

export type MeetingStatus =
  | "draft"
  | "pending_confirmation"
  | "scheduled"
  | "cancelled"
  | "failed";

export type Meeting = {
  id: string;

  title: string;
  agenda?: string;

  startAt: string;
  endAt: string;

  guests: Guest[];

  location?: string;
  meetingUrl?: string;

  notes?: string;

  status: MeetingStatus;

  googleCalendarEventId?: string;

  createdAt: string;
  updatedAt: string;
};

export type ActivityType =
  | "call"
  | "task"
  | "meeting"
  | "note"
  | "memory"
  | "system";

export type Activity = {
  id: string;

  type: ActivityType;

  title: string;
  description?: string;

  result?: string;

  createdAt: string;
};

export type DigitalFriendSettings = {
  phoneNumber?: string;

  language: "english" | "hindi" | "hinglish";

  retryCalls: boolean;

  maxRetries: number;

  retryIntervalMinutes: number;

  quietHoursEnabled: boolean;

  quietHoursStart?: string;
  quietHoursEnd?: string;
};

export type CommunicationPreferences = {
  whatsapp: boolean;
  email: boolean;
  phone: boolean;
  push: boolean;

  taskReminders: boolean;
  meetingReminders: boolean;
  followUps: boolean;
};

export type MorningBriefingSettings = {
  enabled: boolean;

  time: string;

  channels: {
    whatsapp: boolean;
    email: boolean;
    phone: boolean;
  };

  include: {
    meetings: boolean;
    tasks: boolean;
    followUps: boolean;
    notes: boolean;
  };
};

export type IntegrationStatus =
  | "connected"
  | "disconnected"
  | "pending"
  | "error";

export type Integration = {
  id: string;

  provider:
    | "google_calendar"
    | "whatsapp"
    | "email"
    | "digital_friend";

  name: string;

  status: IntegrationStatus;

  connectedAt?: string;

  accountEmail?: string;
};

export type UserProfile = {
  id: string;

  name: string;
  email: string;
  phone?: string;

  timezone: string;

  createdAt: string;
  updatedAt: string;
};