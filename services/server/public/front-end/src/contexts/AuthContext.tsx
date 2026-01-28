"use client";

import React, { createContext, useContext,
    useState, useCallback, useEffect } from "react";
import { api }                         from "@/lib/api";
const STORAGE_PREFIX = "erutalia:";

interface User {
  id         : string;
  email      : string;
  username   : string;
  full_name  : string;
  role       : string;
  is_active  : boolean;
  is_verified: boolean;
}

interface RegisterData {
  email    : string;
  username : string;
  password : string;
  full_name: string;
}

interface AuthContextType {
  user           : User | null;
  isAuthenticated: boolean;
  isLoading      : boolean;
  login          : (email: string, password: string) => Promise<void>;
  register       : (data: RegisterData) => Promise<User>;
  logout         : () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider ({ children }: { children: React.ReactNode }) {
  const [user, setUser]           = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState (true);

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem (`${STORAGE_PREFIX}access_token`);
    if (token) {
      validateToken (token);
    } else {
      setIsLoading (false);
    }
  }, []);

  const validateToken = async (token: string) => {
    try {
      const response = await api.validateToken (token);
      if (response.valid) {
        // In a real app, we'd fetch user details here
        const storedUser = localStorage.getItem (`${STORAGE_PREFIX}user`);
        if (storedUser) {
          setUser (JSON.parse (storedUser));
        }
      } else {
        localStorage.removeItem (`${STORAGE_PREFIX}access_token`);
        localStorage.removeItem (`${STORAGE_PREFIX}refresh_token`);
        localStorage.removeItem (`${STORAGE_PREFIX}user`);
      }
    } catch {
      localStorage.removeItem (`${STORAGE_PREFIX}access_token`);
      localStorage.removeItem (`${STORAGE_PREFIX}refresh_token`);
      localStorage.removeItem (`${STORAGE_PREFIX}user`);
    } finally {
      setIsLoading (false);
    }
  };

  const login = useCallback (async (email: string, password: string) => {
    const response = await api.login (email, password);

    localStorage.setItem (`${STORAGE_PREFIX}access_token`, response.access_token);
    localStorage.setItem (`${STORAGE_PREFIX}refresh_token`, response.refresh_token);
    
    // Mock user data for now - in production this would come from a /me endpoint
    const mockUser: User = {
      id: "user-id",
      email,
      username: email.split ("@")[0],
      full_name: email.split ("@")[0],
      role: "user",
      is_active: true,
      is_verified: false,
    };
    localStorage.setItem (`${STORAGE_PREFIX}user`, JSON.stringify (mockUser));
    setUser (mockUser);
  }, []);

  const register = useCallback (async (data: RegisterData): Promise<User> => {
    const response = await api.register (data);
    /*return {
      id: response.id,
      email: response.email,
      username: response.username,
      full_name: response.full_name,
      role: response.role,
      is_active: response.is_active,
      is_verified: response.is_verified,
    };*/
   return response;
  }, []);

  const logout = useCallback (async () => {
    const refreshToken = localStorage.getItem (`${STORAGE_PREFIX}refresh_token`);
    if (refreshToken) {
      try {
        await api.logout (refreshToken);
      } catch (e) {
        // Continue with local logout even if API fails
        console.error ("Logout API error:", e);
      }
    }
    localStorage.removeItem (`${STORAGE_PREFIX}access_token`);
    localStorage.removeItem (`${STORAGE_PREFIX}refresh_token`);
    localStorage.removeItem (`${STORAGE_PREFIX}user`);
    setUser (null);
  }, []);

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated: !!user, 
      isLoading,
      login, 
      register, 
      logout 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth () {
  const context = useContext (AuthContext);
  if (!context) {
    throw new Error ("useAuth must be used within an AuthProvider");
  }
  return context;
};
