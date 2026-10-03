export const API_ENDPOINTS = {
  auth: {
    login: "/auth/login",
    register: "/auth/register",
    me: "/auth/me",
  },

  tasks: {
    list: "/tasks",
    create: "/tasks",
    detail: (id: string) => `/tasks/${id}`,
    complete: (id: string) => `/tasks/${id}/complete`,
    snooze: (id: string) => `/tasks/${id}/snooze`,
    cancel: (id: string) => `/tasks/${id}/cancel`,
  },

  notes: {
    list: "/notes",
    create: "/notes",
    detail: (id: string) => `/notes/${id}`,
    delete: (id: string) => `/notes/${id}`,
    remember: (id: string) => `/notes/${id}/remember`,
  },

  memory: {
    search: "/memory/search",
    list: "/memory",
  },

  meetings: {
    list: "/meetings",
    create: "/meetings",
    detail: (id: string) => `/meetings/${id}`,
    confirm: (id: string) => `/meetings/${id}/confirm`,
    cancel: (id: string) => `/meetings/${id}/cancel`,
  },

  calendar: {
    events: "/calendar/events",
    sync: "/calendar/sync",
  },

  history: {
    list: "/history",
  },

  digitalFriend: {
    settings: "/digital-friend/settings",
    phoneNumber: "/digital-friend/number",
  },

  preferences: {
    communication: "/preferences/communication",
    briefing: "/preferences/morning-briefing",
  },

  integrations: {
    list: "/integrations",
    connectGoogle: "/integrations/google",
    disconnect: (provider: string) =>
      `/integrations/${provider}/disconnect`,
  },
} as const;