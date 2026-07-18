import type { Job, Candidate, Interview } from '../types'

export const mockJobs: Job[] = [
  {
    id: 'job-1',
    title: 'Senior React Developer',
    department: 'Engineering',
    location: 'Remote (US/Canada)',
    type: 'Full-time',
    status: 'active',
    description: 'We are looking for a Senior React Developer to join our core product team. You will lead the frontend design system implementation, migrate key dashboard components, and build interactive widgets for LLM orchestration.',
    skills: ['React', 'TypeScript', 'Tailwind CSS', 'Zustand', 'Vite', 'GraphQL'],
    resourcesCount: 3,
    applicantsCount: 42,
    aiScreenedCount: 18,
    interviewingCount: 6,
    createdAt: '2026-06-15'
  },
  {
    id: 'job-2',
    title: 'AI / Machine Learning Engineer',
    department: 'AI & Data Science',
    location: 'San Francisco, CA',
    type: 'Full-time',
    status: 'active',
    description: 'Join us to construct production RAG systems, optimize local LLM inference engines (vLLM, Groq), and implement smart chunking/retrieval models using FAISS indices.',
    skills: ['Python', 'PyTorch', 'FastAPI', 'FAISS', 'Groq API', 'RAG Pipelines', 'LangChain'],
    resourcesCount: 5,
    applicantsCount: 31,
    aiScreenedCount: 12,
    interviewingCount: 4,
    createdAt: '2026-06-20'
  },
  {
    id: 'job-3',
    title: 'Product Designer (UI/UX)',
    department: 'Design',
    location: 'Remote (Europe)',
    type: 'Full-time',
    status: 'active',
    description: 'Create high-fidelity SaaS workflows, lead user testing for the candidate portal, and craft stunning micro-interactions and dark mode color palettes.',
    skills: ['Figma', 'UI Design', 'Design Systems', 'Framer Motion', 'User Testing'],
    resourcesCount: 2,
    applicantsCount: 24,
    aiScreenedCount: 8,
    interviewingCount: 2,
    createdAt: '2026-06-28'
  },
  {
    id: 'job-4',
    title: 'DevOps / Infrastructure Engineer',
    department: 'Operations',
    location: 'Hybrid (New York)',
    type: 'Full-time',
    status: 'draft',
    description: 'Maintain Kubernetes clusters, optimize CI/CD pipelines for Python backends and Vite static frontends, and configure VPC security policies.',
    skills: ['AWS', 'Kubernetes', 'Docker', 'GitHub Actions', 'Terraform'],
    resourcesCount: 0,
    applicantsCount: 0,
    aiScreenedCount: 0,
    interviewingCount: 0,
    createdAt: '2026-07-01'
  }
];

export const mockCandidates: Candidate[] = [
  {
    id: 'cand-1',
    name: 'Sarah Connor',
    email: 'sarah.c@sky.net',
    role: 'Senior React Developer',
    matchScore: 94,
    status: 'Interviewing',
    avatarUrl: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150',
    appliedDate: '2026-06-16',
    skillsMatch: ['React', 'TypeScript', 'Tailwind CSS', 'Vite'],
    experienceYears: 6
  },
  {
    id: 'cand-2',
    name: 'Miles Dyson',
    email: 'mdyson@cyberdyne.com',
    role: 'AI / Machine Learning Engineer',
    matchScore: 89,
    status: 'AI Screened',
    avatarUrl: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150',
    appliedDate: '2026-06-21',
    skillsMatch: ['Python', 'FastAPI', 'FAISS', 'RAG Pipelines'],
    experienceYears: 8
  },
  {
    id: 'cand-3',
    name: 'John Connor',
    email: 'john.resistance@future.org',
    role: 'Senior React Developer',
    matchScore: 82,
    status: 'Applied',
    avatarUrl: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=150',
    appliedDate: '2026-06-18',
    skillsMatch: ['React', 'TypeScript', 'GraphQL'],
    experienceYears: 4
  },
  {
    id: 'cand-4',
    name: 'T-800 Cyberdyne',
    email: 't800@cyberdyne.com',
    role: 'DevOps / Infrastructure Engineer',
    matchScore: 97,
    status: 'Offered',
    avatarUrl: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=150',
    appliedDate: '2026-07-02',
    skillsMatch: ['AWS', 'Kubernetes', 'Docker', 'Terraform'],
    experienceYears: 10
  },
  {
    id: 'cand-5',
    name: 'Kate Brewster',
    email: 'kate.b@gmail.com',
    role: 'Product Designer (UI/UX)',
    matchScore: 78,
    status: 'Rejected',
    avatarUrl: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&q=80&w=150',
    appliedDate: '2026-06-29',
    skillsMatch: ['UI Design', 'Figma', 'Design Systems'],
    experienceYears: 3
  }
];

export const mockInterviews: Interview[] = [
  {
    id: 'int-1',
    candidateName: 'Sarah Connor',
    candidateEmail: 'sarah.c@sky.net',
    jobTitle: 'Senior React Developer',
    dateTime: '2026-07-06T14:00:00Z',
    status: 'scheduled',
    durationMinutes: 45,
    meetingLink: 'https://meet.google.com/abc-defg-hij'
  },
  {
    id: 'int-2',
    candidateName: 'Miles Dyson',
    candidateEmail: 'mdyson@cyberdyne.com',
    jobTitle: 'AI / Machine Learning Engineer',
    dateTime: '2026-07-06T16:00:00Z',
    status: 'scheduled',
    durationMinutes: 60,
    meetingLink: 'https://meet.google.com/xyz-pdqr-lmn'
  },
  {
    id: 'int-3',
    candidateName: 'John Connor',
    candidateEmail: 'john.resistance@future.org',
    jobTitle: 'Senior React Developer',
    dateTime: '2026-07-02T10:00:00Z',
    status: 'completed',
    durationMinutes: 45,
    score: 84,
    technicalScore: 88,
    communicationScore: 82,
    problemSolvingScore: 82,
    overallFeedback: 'Strong React architecture concepts. Knows how to use state management well. Communication is precise and direct.'
  },
  {
    id: 'int-4',
    candidateName: 'T-800 Cyberdyne',
    candidateEmail: 't800@cyberdyne.com',
    jobTitle: 'DevOps / Infrastructure Engineer',
    dateTime: '2026-07-04T11:00:00Z',
    status: 'completed',
    durationMinutes: 60,
    score: 96,
    technicalScore: 98,
    communicationScore: 90,
    problemSolvingScore: 100,
    overallFeedback: 'Absolutely flawless system engineering performance. Follows instructions to the exact letter without questions.'
  }
];
