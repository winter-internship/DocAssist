import api from './axios';

export default {
  uploadDocument(formData: FormData) {
    return api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getDocuments(skip = 0, limit = 100) {
    return api.get('/documents/', { params: { skip, limit } });
  },
  getDocument(id: string) {
    return api.get(`/documents/${id}`);
  },
  deleteDocument(id: string) {
    return api.delete(`/documents/${id}`);
  },
};


