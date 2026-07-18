export type UserRole = 'hr' | 'candidate';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  avatarUrl?: string;
  company?: string;
}

export interface Job {
  id: string;
  title: string;
  department: string;
  location: string;
  type: string; // 'Full-time' | 'Contract' etc.
  status: 'active' | 'draft' | 'closed';
  description: string;
  skills: string[];
  resourcesCount: number;
  applicantsCount: number;
  aiScreenedCount: number;
  interviewingCount: number;
  createdAt: string;
}

export interface Candidate {
  id: string;
  name: string;
  email: string;
  role: string; // e.g. "Senior Frontend Engineer"
  matchScore: number;
  status: 'Applied' | 'AI Screened' | 'Interviewing' | 'Offered' | 'Rejected';
  avatarUrl?: string;
  appliedDate: string;
  skillsMatch: string[];
  experienceYears: number;
  phone?: string;
  resumeUrl?: string;
}

export interface Interview {
  id: string;
  candidateName: string;
  candidateEmail: string;
  jobTitle: string;
  dateTime: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  score?: number;
  durationMinutes: number;
  meetingLink?: string;
  overallFeedback?: string;
  technicalScore?: number;
  communicationScore?: number;
  problemSolvingScore?: number;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  createdAt: string;
}
