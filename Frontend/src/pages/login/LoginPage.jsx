import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Truck, Navigation, Users, LineChart, Shield, ShieldCheck, ClipboardList } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import Select from '../../components/ui/Select';
import Card from '../../components/ui/Card';
import authService from '../../services/authService';
import truckImg from '../../assets/truck.png';
import '../../styles/landing.css';

/**
 * LoginPage.
 * Visual composition with scaled elements matching the enterprise control panel design.
 * Integrates RBAC Role selection input and dynamic payload-driven logins.
 */
const LoginPage = () => {
  const { setSession } = useAuth();
  const navigate = useNavigate();

  // View state machine: 'login' | 'otp' | 'forgot' | 'reset'
  const [view, setView] = useState('login');

  // Input states
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [forgotEmail, setForgotEmail] = useState('');
  const [resetOtp, setResetOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // OTP flow context states
  const [targetEmail, setTargetEmail] = useState('');
  const [otpPurpose, setOtpPurpose] = useState('LOGIN');
  const [cooldown, setCooldown] = useState(0);

  // Status feedback states
  const [error, setError] = useState('');
  const [infoMessage, setInfoMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Cooldown timer countdown hook
  useEffect(() => {
    let interval = null;
    if (cooldown > 0) {
      interval = setInterval(() => {
        setCooldown((prev) => prev - 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [cooldown]);

  // Dynamic error formatting
  const getErrorMessage = (errorObj) => {
    if (errorObj.response && errorObj.response.data) {
      return errorObj.response.data.message || 'Operation failed. Please check inputs.';
    }
    return errorObj.message || 'A connection error occurred. Please try again.';
  };

  // Validators
  const validateEmail = (emailStr) => {
    if (!emailStr) return 'Email is required.';
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(emailStr)) return 'Please enter a valid email address.';
    return null;
  };

  const validateNewPassword = (pwd) => {
    if (!pwd) return 'New password is required.';
    if (pwd.length < 8) return 'Password must be at least 8 characters long.';
    if (!/[A-Z]/.test(pwd)) return 'Password must contain at least one uppercase letter.';
    if (!/[a-z]/.test(pwd)) return 'Password must contain at least one lowercase letter.';
    if (!/\d/.test(pwd)) return 'Password must contain at least one number.';
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) return 'Password must contain at least one special character.';
    return null;
  };

  // Submit Handlers
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setInfoMessage('');

    const emailErr = validateEmail(email);
    if (emailErr) {
      setError(emailErr);
      return;
    }
    if (!password) {
      setError('Password is required.');
      return;
    }
    if (!selectedRole) {
      setError('Please select your role.');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await authService.login({ 
        email, 
        password, 
        role: selectedRole 
      });

      if (response.success) {
        if (response.data.requires_otp) {
          setTargetEmail(email);
          setOtpPurpose('LOGIN');
          setView('otp');
          const retryAfter = response.data.retry_after || 45;
          setCooldown(retryAfter);
          setInfoMessage('A verification code has been sent to your email.');
        } else {
          // Direct login
          const token = response.data.access_token;
          localStorage.setItem('transitops_token', token);

          // Get profile details
          const meResponse = await authService.getMe();
          if (meResponse.success) {
            const user = meResponse.data.user;
            setSession(user, user.role, token);

            const dashboardSlug = user.role.toLowerCase().replace(/\s+/g, '-');
            navigate(`/${dashboardSlug}/dashboard`);
          } else {
            setError(meResponse.message || 'Failed to retrieve profile metadata.');
            localStorage.removeItem('transitops_token');
          }
        }
      } else {
        setError(response.message || 'Login failed.');
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setInfoMessage('');

    if (!otpCode || otpCode.length !== 6 || !/^\d{6}$/.test(otpCode)) {
      setError('OTP must be exactly 6 digits.');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await authService.verifyOtp(targetEmail, otpPurpose, otpCode);
      if (response.success) {
        const token = response.data.access_token;
        localStorage.setItem('transitops_token', token);

        const meResponse = await authService.getMe();
        if (meResponse.success) {
          const user = meResponse.data.user;
          setSession(user, user.role, token);

          const dashboardSlug = user.role.toLowerCase().replace(/\s+/g, '-');
          navigate(`/${dashboardSlug}/dashboard`);
        } else {
          setError(meResponse.message || 'Failed to retrieve profile details after verification.');
          localStorage.removeItem('transitops_token');
        }
      } else {
        setError(response.message || 'OTP verification failed.');
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResendOTP = async () => {
    setError('');
    setInfoMessage('');
    try {
      const response = await authService.resendOtp(targetEmail, otpPurpose);
      if (response.success) {
        setInfoMessage('A new verification code has been sent.');
        const retryAfter = response.data?.retry_after || 45;
        setCooldown(retryAfter);
      } else {
        setError(response.message || 'Failed to resend verification code.');
      }
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const handleForgotSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setInfoMessage('');

    const emailErr = validateEmail(forgotEmail);
    if (emailErr) {
      setError(emailErr);
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await authService.forgotPassword(forgotEmail);
      if (response.success) {
        setTargetEmail(forgotEmail);
        setOtpPurpose('FORGOT_PASSWORD');
        setView('reset');
        setInfoMessage('A password recovery code has been sent to your email.');
      } else {
        setError(response.message || 'Failed to trigger password recovery.');
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResetSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setInfoMessage('');

    if (!resetOtp || resetOtp.length !== 6 || !/^\d{6}$/.test(resetOtp)) {
      setError('OTP must be exactly 6 digits.');
      return;
    }

    const passwordErr = validateNewPassword(newPassword);
    if (passwordErr) {
      setError(passwordErr);
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await authService.resetPassword(targetEmail, resetOtp, newPassword, confirmPassword);
      if (response.success) {
        setResetOtp('');
        setNewPassword('');
        setConfirmPassword('');
        setForgotEmail('');
        setView('login');
        setInfoMessage('Password reset successfully. You can now sign in with your new password.');
      } else {
        setError(response.message || 'Password reset failed.');
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  // Helper transitions
  const transitionToForgot = () => {
    setError('');
    setInfoMessage('');
    setView('forgot');
  };

  const transitionToLogin = () => {
    setError('');
    setInfoMessage('');
    setView('login');
  };

  return (
    <div className="min-h-screen md:h-screen md:max-h-screen bg-bg-cream flex flex-col md:flex-row w-full font-sans overflow-y-auto md:overflow-hidden">
      
      {/* Left Column Branding Panel (46% Width, baseline aligned md:pt-20, vertical flow) */}
      <div className="w-full md:w-[46%] bg-bg-cream border-r border-border-warm/20 flex flex-col justify-start p-8 md:p-12 md:pt-20 select-none shrink-0 md:h-full space-y-6">
        
        {/* Brand Logo header */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-primary flex items-center justify-center text-card-white font-bold text-lg">
            T
          </div>
          <span className="text-lg font-bold tracking-tight text-text-primary">TransitOps</span>
        </div>
        
        {/* Headings container with compressed vertical spacing */}
        <div className="space-y-4 pt-2">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-[10px] font-bold uppercase tracking-wider select-none">
            Odoo Hackathon 2026
          </span>
          <h2 className="text-5xl lg:text-6xl font-black text-text-primary tracking-tighter leading-[1.02] select-none">
            Smart Transport <br />
            <span className="text-primary block mt-1.5">Operations <br /> Platform</span>
          </h2>
          <p className="text-xs text-text-secondary leading-relaxed max-w-sm font-medium pt-1">
            TransitOps helps organizations efficiently manage fleet operations, transportation workflows, and business logistics through a centralized platform.
          </p>
        </div>

        {/* Action Button */}
        <div>
          <Button 
            onClick={() => document.getElementById('email-input')?.focus()}
            className="px-6 py-2.5 text-xs font-bold bg-primary hover:bg-secondary text-card-white rounded-[var(--radius-input)] transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] shadow-md hover:shadow-lg flex items-center gap-2 w-fit focus:ring-2 focus:ring-primary focus:outline-none"
          >
            <span>Login</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Button>
        </div>

        {/* Anchored lower-third mascot with balanced spacing above/below */}
        <div className="relative select-none hidden md:block w-full pt-4 pb-12 mt-6">
          <div className="border-b-[3px] border-border-warm w-full absolute bottom-12 left-0" />
          <img 
            src={truckImg} 
            alt="TransitOps Truck mascot" 
            className="w-72 lg:w-80 h-auto object-contain relative z-10 -mb-1 -ml-8 md:-ml-12 hero-truck-image mix-blend-multiply" 
          />
        </div>
      </div>

      {/* Right Column Form Panel (54% Width, aligned top-left on desktop via md:pl-16 md:pt-14) */}
      <div className="w-full md:w-[54%] flex items-start md:items-start justify-center md:justify-start p-6 md:p-12 md:pl-16 md:pt-14 bg-bg-cream/20 md:h-full shrink-0">
        <Card className="relative overflow-hidden w-full max-w-[530px] bg-card-warm border border-border-warm shadow-login p-10 rounded-[var(--radius-card)]">
          
          {/* Decorative warm accent dots overlays */}
          <div className="absolute top-5 right-5 grid grid-cols-4 gap-1.5 opacity-30 select-none pointer-events-none" aria-hidden="true">
            {Array.from({ length: 16 }).map((_, i) => (
              <div key={i} className="w-1 h-1 rounded-full bg-[#C2B797]" />
            ))}
          </div>
          <div className="absolute bottom-5 left-5 grid grid-cols-4 gap-1.5 opacity-30 select-none pointer-events-none" aria-hidden="true">
            {Array.from({ length: 16 }).map((_, i) => (
              <div key={i} className="w-1 h-1 rounded-full bg-[#C2B797]" />
            ))}
          </div>

          {/* View: Standard Login Card */}
          {view === 'login' && (
            <div className="space-y-6">
              <div className="space-y-1">
                <h3 className="text-xl font-black text-text-primary tracking-tight">Welcome back</h3>
                <p className="text-xs text-text-secondary font-medium">Login to your TransitOps account</p>
              </div>

              <form onSubmit={handleLoginSubmit} className="space-y-4">
                {error && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-primary/5 border border-primary/20 text-xs font-semibold text-primary">
                    ❌ {error}
                  </div>
                )}
                {infoMessage && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-status-avail-bg border border-status-avail-text/20 text-xs font-semibold text-status-avail-text">
                    ✓ {infoMessage}
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Email address
                  </label>
                  <Input
                    id="email-input"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="raven.k@transitops.in"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Password
                  </label>
                  <Input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                </div>

                {/* RBAC Role Selector Dropdown */}
                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Role
                  </label>
                  <Select
                    value={selectedRole}
                    onChange={(e) => setSelectedRole(e.target.value)}
                    required
                  >
                    <option value="" disabled hidden>Select your role</option>
                    <option value="Fleet Manager">Fleet Manager</option>
                    <option value="Dispatcher">Dispatcher</option>
                    <option value="Safety Officer">Safety Officer</option>
                    <option value="Financial Analyst">Financial Analyst</option>
                  </Select>
                </div>

                <div className="flex items-center justify-between text-xs pt-2">
                  <label className="flex items-center gap-2 font-semibold text-text-secondary select-none cursor-pointer">
                    <input 
                      type="checkbox" 
                      className="w-4 h-4 rounded border-border-warm text-primary focus:ring-primary focus:ring-offset-0 focus:outline-none cursor-pointer"
                    />
                    Remember me
                  </label>
                  <button 
                    type="button" 
                    className="font-bold text-primary hover:underline focus:outline-none"
                    onClick={transitionToForgot}
                  >
                    Forgot password?
                  </button>
                </div>

                <div className="pt-2">
                  <Button 
                    type="submit" 
                    className="w-full h-11" 
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Signing In...' : 'Login'}
                  </Button>
                </div>
              </form>

              {/* Enterprise Grade Security widget - Renders directly below Login button */}
              <div className="rounded-[var(--radius-card)] bg-bg-cream/40 border border-border-warm p-4.5 flex gap-3 text-left shadow-xs">
                <div className="w-10 h-10 rounded-lg bg-[#E0F2F1] text-[#00695C] flex items-center justify-center shrink-0 select-none">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div className="space-y-0.5">
                  <h4 className="text-xs font-bold text-text-primary">Enterprise Grade Security</h4>
                  <p className="text-[10px] text-text-secondary leading-normal font-medium">Your data is protected with industry-leading security and compliance standards.</p>
                </div>
              </div>

              {/* Role Access Information Panel (Replacing Platform Highlights) */}
              <div className="rounded-[var(--radius-card)] bg-bg-cream/40 border border-border-warm p-5 text-left shadow-xs space-y-3.5">
                <h4 className="text-[10px] font-bold text-text-secondary uppercase tracking-wider select-none">Role Access</h4>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 text-xs">
                    <div className="w-7 h-7 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0 select-none">
                      <Truck className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <span className="font-bold text-text-primary text-xs">Fleet Manager</span>
                      <span className="text-text-secondary font-medium text-[11px] block truncate">— Fleet, Maintenance, Analytics</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-xs">
                    <div className="w-7 h-7 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0 select-none">
                      <ClipboardList className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <span className="font-bold text-text-primary text-xs">Dispatcher</span>
                      <span className="text-text-secondary font-medium text-[11px] block truncate">— Trips, Fleet View, Fuel & Expenses</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-xs">
                    <div className="w-7 h-7 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0 select-none">
                      <Shield className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <span className="font-bold text-text-primary text-xs">Safety Officer</span>
                      <span className="text-text-secondary font-medium text-[11px] block truncate">— Drivers, Compliance, Trip View</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-xs">
                    <div className="w-7 h-7 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0 select-none">
                      <LineChart className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <span className="font-bold text-text-primary text-xs">Financial Analyst</span>
                      <span className="text-text-secondary font-medium text-[11px] block truncate">— Analytics, Reports</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* View: OTP Verification Card */}
          {view === 'otp' && (
            <div className="space-y-6">
              <div className="space-y-1.5">
                <h3 className="text-xl font-black text-text-primary tracking-tight">Two-Factor OTP Verification</h3>
                <p className="text-xs text-text-secondary font-medium">Verify your login attempt below</p>
              </div>

              <form onSubmit={handleOtpSubmit} className="space-y-4">
                {error && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-primary/5 border border-primary/20 text-xs font-semibold text-primary">
                    ❌ {error}
                  </div>
                )}
                {infoMessage && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-status-avail-bg border border-status-avail-text/20 text-xs font-semibold text-status-avail-text">
                    ✓ {infoMessage}
                  </div>
                )}

                <div className="p-3.5 bg-bg-cream/40 border border-border-warm rounded-[var(--radius-card)] text-xs text-text-secondary leading-relaxed">
                  We sent a 6-digit code to <strong className="text-text-primary">{targetEmail}</strong>. Enter it below to complete authentication.
                </div>

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Verification Code
                  </label>
                  <Input
                    type="text"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    placeholder="123456"
                    className="text-center tracking-widest text-lg font-black"
                    maxLength={6}
                    required
                  />
                </div>

                <div className="flex flex-col sm:flex-row gap-3 pt-4">
                  <Button 
                    type="button" 
                    variant="secondary" 
                    className="flex-1"
                    onClick={transitionToLogin}
                  >
                    Cancel
                  </Button>
                  <Button 
                    type="submit" 
                    className="flex-1" 
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Verifying...' : 'Verify Code'}
                  </Button>
                </div>

                <div className="text-center pt-3 border-t border-border-warm">
                  <button
                    type="button"
                    disabled={cooldown > 0}
                    onClick={handleResendOTP}
                    className={`text-xs font-bold ${cooldown > 0 ? 'text-text-secondary/60 cursor-not-allowed' : 'text-primary hover:underline'}`}
                  >
                    {cooldown > 0 ? `Resend Code in ${cooldown}s` : 'Resend Code'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* View: Forgot Password Card */}
          {view === 'forgot' && (
            <div className="space-y-6">
              <div className="space-y-1.5">
                <h3 className="text-xl font-black text-text-primary tracking-tight">Password Recovery</h3>
                <p className="text-xs text-text-secondary font-medium">Reset your secure login access</p>
              </div>

              <form onSubmit={handleForgotSubmit} className="space-y-4">
                {error && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-primary/5 border border-primary/20 text-xs font-semibold text-primary">
                    ❌ {error}
                  </div>
                )}

                <div className="p-3.5 bg-bg-cream/40 border border-border-warm rounded-[var(--radius-card)] text-xs text-text-secondary leading-relaxed">
                  Enter your email address. We will verify your account and send a 6-digit OTP code to authorize password recovery.
                </div>

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Email Address
                  </label>
                  <Input
                    type="email"
                    value={forgotEmail}
                    onChange={(e) => setForgotEmail(e.target.value)}
                    placeholder="name@transitops.in"
                    required
                  />
                </div>

                <div className="flex flex-col sm:flex-row gap-3 pt-4">
                  <Button 
                    type="button" 
                    variant="secondary" 
                    className="flex-1"
                    onClick={transitionToLogin}
                  >
                    Back to Login
                  </Button>
                  <Button 
                    type="submit" 
                    className="flex-1" 
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Sending...' : 'Send OTP'}
                  </Button>
                </div>
              </form>
            </div>
          )}

          {/* View: Reset Password Card */}
          {view === 'reset' && (
            <div className="space-y-6">
              <div className="space-y-1.5">
                <h3 className="text-xl font-black text-text-primary tracking-tight">Set New Password</h3>
                <p className="text-xs text-text-secondary font-medium">Create a new secure password</p>
              </div>

              <form onSubmit={handleResetSubmit} className="space-y-4">
                {error && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-primary/5 border border-primary/20 text-xs font-semibold text-primary">
                    ❌ {error}
                  </div>
                )}
                {infoMessage && (
                  <div className="p-3.5 rounded-[var(--radius-input)] bg-status-avail-bg border border-status-avail-text/20 text-xs font-semibold text-status-avail-text">
                    ✓ {infoMessage}
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Recovery OTP Code
                  </label>
                  <Input
                    type="text"
                    value={resetOtp}
                    onChange={(e) => setResetOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    placeholder="123456"
                    className="text-center tracking-widest text-base font-bold"
                    maxLength={6}
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    New Password
                  </label>
                  <Input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2 select-none">
                    Confirm Password
                  </label>
                  <Input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                </div>

                <div className="p-3.5 bg-bg-cream/40 border border-border-warm rounded-[var(--radius-card)] text-[10px] text-text-secondary leading-relaxed space-y-1 select-none">
                  <span className="font-bold text-text-primary block mb-0.5">Password Requirements:</span>
                  <p>• At least 8 characters long</p>
                  <p>• Include uppercase & lowercase characters</p>
                  <p>• Include at least one number & special symbol</p>
                </div>

                <div className="flex flex-col sm:flex-row gap-3 pt-4">
                  <Button 
                    type="button" 
                    variant="secondary" 
                    className="flex-1"
                    onClick={transitionToLogin}
                  >
                    Cancel
                  </Button>
                  <Button 
                    type="submit" 
                    className="flex-1" 
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Resetting...' : 'Reset Password'}
                  </Button>
                </div>
              </form>
            </div>
          )}

        </Card>
      </div>

    </div>
  );
};

export default LoginPage;
