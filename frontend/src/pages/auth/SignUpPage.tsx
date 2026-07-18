import * as React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../stores/auth-store'
import { useNotificationStore } from '../../stores/notification-store'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'

export const SignUpPage: React.FC = () => {
  const navigate = useNavigate();
  const signup = useAuthStore((state) => state.signup);
  const addToast = useNotificationStore((state) => state.addToast);

  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [role, setRole] = React.useState<'hr' | 'candidate'>('hr');
  const [company, setCompany] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email) {
      addToast('Please fill in all fields', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const user = await signup(name, email, role, role === 'hr' ? company : undefined);
      addToast(`Account created successfully! Welcome, ${user.name}.`, 'success');
      if (user.role === 'hr') {
        navigate('/hr/dashboard');
      } else {
        navigate('/candidate/dashboard');
      }
    } catch (err: any) {
      addToast(err.message || 'Signup failed', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-col gap-6">
      <div className="flex flex-col text-center gap-1.5">
        <h1 className="text-3xl font-extrabold text-white tracking-tight bg-gradient-to-r from-primary-400 to-indigo-400 bg-clip-text text-transparent">
          Create an account
        </h1>
        <p className="text-slate-400 text-sm">
          Get started with Evalora Interview Intelligence today
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          type="text"
          label="Full Name"
          placeholder="John Doe"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <Input
          type="email"
          label="Email Address"
          placeholder="name@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <Select
          label="I want to sign up as"
          value={role}
          onChange={(e) => setRole(e.target.value as 'hr' | 'candidate')}
          options={[
            { value: 'hr', label: 'HR Professional / Recruiter' },
            { value: 'candidate', label: 'Candidate / Job Seeker' }
          ]}
        />

        {role === 'hr' && (
          <Input
            type="text"
            label="Company Name"
            placeholder="Acme Corp"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            required
          />
        )}

        <Button type="submit" className="w-full py-3 mt-2" isLoading={isLoading}>
          Create Account
        </Button>
      </form>

      <div className="text-center text-sm text-slate-400 mt-2">
        Already have an account?{' '}
        <Link to="/login" className="text-primary-400 hover:text-primary-300 font-semibold">
          Sign in
        </Link>
      </div>
    </div>
  );
};
