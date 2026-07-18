import * as React from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Button } from '../../components/ui/Button'
import { mockInterviews } from '../../lib/mock-data'
import { useAuthStore } from '../../stores/auth-store'
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts'

export const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();

  const skillsData = [
    { subject: 'Technical', A: 85, fullMark: 100 },
    { subject: 'Coding Skill', A: 90, fullMark: 100 },
    { subject: 'System Design', A: 75, fullMark: 100 },
    { subject: 'Communication', A: 88, fullMark: 100 },
    { subject: 'Problem Solving', A: 92, fullMark: 100 }
  ];

  return (
    <div className="flex flex-col gap-8">
      {/* Title Greeting Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">
          Welcome back, {user?.name || 'Candidate'}!
        </h1>
        <p className="text-slate-400 text-sm mt-1">Review your scheduled interviews, track your assessment states, and browse AI feedback.</p>
      </div>

      {/* Main Content Split Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Next Scheduled Assessment Card */}
        <Card className="lg:col-span-2 flex flex-col justify-between" glowColor="primary">
          <CardHeader>
            <div className="flex items-center justify-between">
              <Badge variant="primary" size="md">Upcoming Assessment</Badge>
              <span className="text-xs text-slate-500 font-medium">Google Meet</span>
            </div>
            <CardTitle className="text-2xl mt-4">Technical System Architecture</CardTitle>
            <CardDescription className="mt-1">Role: Senior React Developer</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 rounded-xl bg-slate-900 border border-slate-800/60">
              <div>
                <p className="text-xxs font-semibold text-slate-500 uppercase tracking-wider">Date</p>
                <p className="text-sm font-semibold text-white mt-1">July 06, 2026</p>
              </div>
              <div>
                <p className="text-xxs font-semibold text-slate-500 uppercase tracking-wider">Time</p>
                <p className="text-sm font-semibold text-white mt-1">2:00 PM EST</p>
              </div>
              <div>
                <p className="text-xxs font-semibold text-slate-500 uppercase tracking-wider">Duration</p>
                <p className="text-sm font-semibold text-white mt-1">45 Minutes</p>
              </div>
              <div>
                <p className="text-xxs font-semibold text-slate-500 uppercase tracking-wider">Interviewer</p>
                <p className="text-sm font-semibold text-white mt-1">Evalora AI Agent</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <a href="https://meet.google.com/abc-defg-hij" target="_blank" rel="noopener noreferrer" className="flex-1">
                <Button className="w-full py-3 flex items-center justify-center gap-2">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Enter Interview Lobby
                </Button>
              </a>
              <Button variant="outline" className="py-3">
                Reschedule
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* AI Performance Radar Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Skills Profile</CardTitle>
            <CardDescription>AI assessed strengths based on past completed exercises.</CardDescription>
          </CardHeader>
          <CardContent className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={skillsData}>
                <PolarGrid stroke="#1e293b" />
                <PolarAngleAxis dataKey="subject" stroke="#94a3b8" fontSize={11} />
                <PolarRadiusAxis stroke="#475569" angle={30} domain={[0, 100]} fontSize={9} />
                <Radar name="Candidate" dataKey="A" stroke="#4f5bf6" fill="#4f5bf6" fillOpacity={0.2} />
              </RadarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Grid containing previous assessments and insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Previous Assessments List */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Completed Assessments</CardTitle>
            <CardDescription>View scores, evaluations, and overall performance history.</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-800/40">
              {mockInterviews.filter(i => i.status === 'completed').map((int) => (
                <div key={int.id} className="p-5 flex items-center justify-between hover:bg-white/5 transition-colors duration-150">
                  <div>
                    <h4 className="text-sm font-semibold text-white">{int.jobTitle}</h4>
                    <p className="text-xs text-slate-500 mt-1">Completed on {int.dateTime.split('T')[0]}</p>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <p className="text-xs text-slate-500">Overall Score</p>
                      <p className="text-lg font-bold text-emerald-400 mt-0.5">{int.score}%</p>
                    </div>
                    <Button variant="outline" size="sm">
                      Details
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* AI Constructive Feedback */}
        <Card>
          <CardHeader>
            <CardTitle>AI Performance Insights</CardTitle>
            <CardDescription>Tailored feedback points gathered from previous tests.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800/60 flex items-start gap-3">
              <span className="text-emerald-400 mt-0.5">✔</span>
              <div>
                <h5 className="text-xs font-bold text-white uppercase tracking-wider">Strong Soft Skills</h5>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">Exhibited excellent flow and clarity of structure during system design exercises.</p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800/60 flex items-start gap-3">
              <span className="text-amber-400 mt-0.5">ℹ</span>
              <div>
                <h5 className="text-xs font-bold text-white uppercase tracking-wider">Improvement Area</h5>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">Keep watch on algorithm complexity details when implementing nested loop handlers.</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
export default DashboardPage;
