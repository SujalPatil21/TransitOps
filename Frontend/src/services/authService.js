import api from './api/axios';

/**
 * Service to execute auth operations against backend REST APIs.
 */

export const login = async ({ email, password }) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const verifyOtp = async (email, purpose, otp) => {
  const response = await api.post('/auth/verify-otp', { email, purpose, otp });
  return response.data;
};

export const resendOtp = async (email, purpose) => {
  const response = await api.post('/auth/resend-otp', { email, purpose });
  return response.data;
};

export const forgotPassword = async (email) => {
  const response = await api.post('/auth/forgot-password', { email });
  return response.data;
};

export const resetPassword = async (email, otp, new_password, confirm_password) => {
  const response = await api.post('/auth/reset-password', { email, otp, new_password, confirm_password });
  return response.data;
};

export const getMe = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export default {
  login,
  verifyOtp,
  resendOtp,
  forgotPassword,
  resetPassword,
  getMe
};
