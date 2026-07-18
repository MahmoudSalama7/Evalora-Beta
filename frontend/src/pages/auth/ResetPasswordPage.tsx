import * as React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useNotificationStore } from '../../stores/notification-store'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'

export const ResetPasswordPage: React.FC = () => {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  const [password, setPassword] = React.useState('');
  const [confirmPassword, setConfirmPassword] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      addToast('Passwords do not match', 'error');
      return;
    }

    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 800));
    setIsLoading(false);
    addToast('Password has been reset successfully.', 'success');
    navigate('/login');
  };

  return (
    <div className="w-full flex flex-col gap-6">
      <div className="flex flex-col text-center gap-1.5">
        <h1 className="text-3xl font-extrabold text-white tracking-tight bg-gradient-to-r from-primary-400 to-indigo-400 bg-clip-text text-transparent">
          Create new password
        </h1>
        <p className="text-slate-400 text-sm">
          Please enter your new password below
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          type="password"
          label="New Password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Input
          type="password"
          label="Confirm New Password"
          placeholder="••••••••"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        <Button type="submit" className="w-full py-3 mt-2" isLoading={isLoading}>
          Reset Password
        </Button>
      </form>

      <div className="text-center text-sm text-slate-400 mt-2">
        <Link to="/login" className="text-primary-400 hover:text-primary-300 font-semibold">
          Back to Login
        </Link>
      </div>
    </div>
  );
};
export default ResetPasswordPage;
