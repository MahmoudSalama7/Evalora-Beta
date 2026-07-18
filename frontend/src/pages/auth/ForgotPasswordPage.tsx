import * as React from 'react'
import { Link } from 'react-router-dom'
import { useNotificationStore } from '../../stores/notification-store'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'

export const ForgotPasswordPage: React.FC = () => {
  const addToast = useNotificationStore((state) => state.addToast);
  const [email, setEmail] = React.useState('');
  const [isSubmitted, setIsSubmitted] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setIsLoading(true);
    // Simulate API request
    await new Promise((resolve) => setTimeout(resolve, 800));
    setIsLoading(false);
    setIsSubmitted(true);
    addToast('Password reset link sent to your email.', 'success');
  };

  if (isSubmitted) {
    return (
      <div className="w-full flex flex-col gap-6 text-center">
        <div className="flex flex-col gap-2">
          <div className="w-12 h-12 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-2">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-white">Check your email</h1>
          <p className="text-slate-400 text-sm max-w-sm mx-auto leading-relaxed">
            We have sent password reset instructions to <span className="text-white font-semibold">{email}</span>.
          </p>
        </div>
        <Link to="/login" className="w-full">
          <Button variant="outline" className="w-full">
            Back to login
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-6">
      <div className="flex flex-col text-center gap-1.5">
        <h1 className="text-3xl font-extrabold text-white tracking-tight bg-gradient-to-r from-primary-400 to-indigo-400 bg-clip-text text-transparent">
          Reset password
        </h1>
        <p className="text-slate-400 text-sm">
          Enter your email and we'll send you a recovery link
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          type="email"
          label="Email Address"
          placeholder="name@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <Button type="submit" className="w-full py-3 mt-2" isLoading={isLoading}>
          Send Recovery Link
        </Button>
      </form>

      <div className="text-center text-sm text-slate-400 mt-2">
        Remembered your password?{' '}
        <Link to="/login" className="text-primary-400 hover:text-primary-300 font-semibold">
          Sign in
        </Link>
      </div>
    </div>
  );
};
export default ForgotPasswordPage;
