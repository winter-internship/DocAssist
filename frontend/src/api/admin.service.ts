import api from './axios';

export interface AdminMetrics {
  users: number;
  docs: number;
  queue: number;
  qaToday: number;
}

export interface UserItem {
  id: string;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface DocItem {
  id: string;
  title: string;
  file_type: string;
  status: string;
  created_at: string;
  user_id: string;
}

export default {
  async getMetrics(): Promise<{ data: AdminMetrics }> {
    return api.get('/admin/metrics');
  },
  
  async getUsers(params?: { skip?: number; limit?: number }) {
      return api.get<UserItem[]>('/admin/users', { params });
  },
  
  async getDocuments(params?: { skip?: number; limit?: number }) {
      return api.get<DocItem[]>('/admin/documents', { params });
  }
};
