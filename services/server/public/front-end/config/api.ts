// API Configuration
export const apiConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  endpoints: {
    // Auth endpoints
    login: "/api/auth/login",
    register: "/api/auth/register",
    logout: "/api/auth/logout",
    me: "/api/auth/me",

    // Chat endpoints
    chats: "/api/chats",
    chatMessages: (chatId: string) => `/api/chats/${chatId}/messages`,
    sendMessage: "/api/chat/send",

    // Admin endpoints
    users: "/api/admin/users",
    deleteUser: (userId: string) => `/api/admin/users/${userId}`,
    createUser: "/api/admin/users",
  },
  timeout: 30000, // 30 seconds
}

export type ApiConfig = typeof apiConfig
