import api from './api/axios';

/**
 * Service to execute auth operations against backend REST APIs.
 * Temporarily running in Mock Mode to support offline hackathon deployment.
 * Payload structures and return shapes match backend specifications.
 */

// Helper to determine user role from email address dynamically if not supplied
const getRoleFromEmail = (email) => {
  const norm = email.toLowerCase();
  if (norm.includes('dispatcher')) {
    return 'Dispatcher';
  }
  if (norm.includes('safety')) {
    return 'Safety Officer';
  }
  if (norm.includes('analyst') || norm.includes('finance')) {
    return 'Financial Analyst';
  }
  return 'Fleet Manager'; // Default role
};

/**
 * Simulates POST /auth/login.
 * Consumes single object payload to mirror future FastAPI backend contract.
 */
export const login = async ({ email, password, role }) => {
  // Simulate network latency (600ms)
  await new Promise((resolve) => setTimeout(resolve, 600));

  const norm = email.toLowerCase();
  const selectedRole = role || getRoleFromEmail(email);
  const username = email.split('@')[0] || 'demo_user';

  // Check if testing OTP verification workflow specifically
  if (norm.includes('otp')) {
    return {
      success: true,
      message: 'Verification code sent to your email.',
      data: {
        requires_otp: true,
        retry_after: 45
      }
    };
  }

  // Regular direct login success path
  const mockUser = {
    id: 1,
    username,
    email,
    role: selectedRole,
    is_verified: true
  };
  localStorage.setItem('transitops_mock_user', JSON.stringify(mockUser));

  return {
    success: true,
    message: 'Login successful.',
    data: {
      requires_otp: false,
      access_token: 'mock-jwt-access-token-string',
      token_type: 'bearer',
      role: selectedRole,
      username
    }
  };
};

/**
 * Simulates POST /auth/verify-otp.
 */
export const verifyOtp = async (email, purpose, otp) => {
  // Simulate network latency (500ms)
  await new Promise((resolve) => setTimeout(resolve, 500));

  const role = getRoleFromEmail(email);
  const username = email.split('@')[0] || 'demo_user';

  const mockUser = {
    id: 1,
    username,
    email,
    role,
    is_verified: true
  };
  localStorage.setItem('transitops_mock_user', JSON.stringify(mockUser));

  return {
    success: true,
    message: 'OTP verified successfully.',
    data: {
      access_token: 'mock-jwt-access-token-string',
      token_type: 'bearer',
      role,
      username
    }
  };
};

/**
 * Simulates POST /auth/resend-otp.
 */
export const resendOtp = async (email, purpose) => {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return {
    success: true,
    message: 'OTP code resent successfully.',
    data: {
      retry_after: 45
    }
  };
};

/**
 * Simulates POST /auth/forgot-password.
 */
export const forgotPassword = async (email) => {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return {
    success: true,
    message: 'Password recovery OTP sent.'
  };
};

/**
 * Simulates POST /auth/reset-password.
 */
export const resetPassword = async (email, otp, new_password, confirm_password) => {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return {
    success: true,
    message: 'Password reset successfully.'
  };
};

/**
 * Simulates GET /auth/me.
 */
export const getMe = async () => {
  // Simulate network latency (100ms)
  await new Promise((resolve) => setTimeout(resolve, 100));

  const mockUserStr = localStorage.getItem('transitops_mock_user');
  const user = mockUserStr ? JSON.parse(mockUserStr) : {
    id: 1,
    username: 'demo_user',
    email: 'demo@transitops.in',
    role: 'Fleet Manager',
    is_verified: true
  };

  return {
    success: true,
    message: 'User profile fetched.',
    data: {
      user
    }
  };
};

export default {
  login,
  verifyOtp,
  resendOtp,
  forgotPassword,
  resetPassword,
  getMe
};
