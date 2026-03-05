export const api = {
  validateToken: async (token: string) => ({ valid: false }),
  login: async (email: string, password: string) => ({ access_token: "", refresh_token: "" }),
  register: async (data: any) => data,
  logout: async (refreshToken: string) => {return { success: false }; },
};
