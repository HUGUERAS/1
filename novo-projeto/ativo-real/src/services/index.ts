/**
 * Placeholder API - será conectado ao backend real
 */

export const apiClient = {
  login: async (email: string, password: string) => {
    return { access_token: 'mock_token', user: { id: '1', email } };
  },
  
  getProjects: async () => {
    return [];
  },
  
  createProject: async (data: any) => {
    return { id: '1', ...data };
  }
};
