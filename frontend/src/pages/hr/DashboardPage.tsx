import * as React from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '../../components/ui/Table'
import { mockJobs, mockCandidates, mockInterviews } from '../../lib/mock-data'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export const DashboardPage: React.FC = () => {
  // Chart Data
  const funnelData = [
    { name: 'Applied', count: 120 },
    { name: 'AI Screened', count: 78 },
    { name: 'Interviewing', count: 24 },
    { name: 'Offered', count: 8 },
    { name: 'Hired', count: 5 }
  ];

  const activityData = [
    { date: 'Mon', interviews: 2 },
    { date: 'Tue', interviews: 5 },
    { date: 'Wed', interviews: 7 },
    { date: 'Thu', interviews: 4 },
    { date: 'Fri', interviews: 8 }
  ];

  return (
    <div className="flex flex-col gap-8">
      {/* Page Title Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Recruiting Insights</h1>
        <p className="text-slate-400 text-sm mt-1">Real-time overview of your hiring funnel, active jobs, and pipeline health.</p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card glowColor="primary">
          <CardContent className="p-6 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Jobs</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {mockJobs.filter(j => j.status === 'active').length}
              </h3>
            </div>
            <div className="w-12 h-12 rounded-lg bg-primary-500/10 text-primary-400 flex items-center justify-center border border-primary-500/20">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </CardContent>
        </Card>

        <Card glowColor="success">
          <CardContent className="p-6 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Candidates</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {mockCandidates.length}
              </h3>
            </div>
            <div className="w-12 h-12 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
          </CardContent>
        </Card>

        <Card glowColor="warning">
          <CardContent className="p-6 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Interviews</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {mockInterviews.filter(i => i.status === 'scheduled').length}
              </h3>
            </div>
            <div className="w-12 h-12 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center border border-amber-500/20">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </CardContent>
        </Card>

        <Card glowColor="none">
          <CardContent className="p-6 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">AI Screening Match Rate</p>
              <h3 className="text-3xl font-bold text-white mt-2">87.5%</h3>
            </div>
            <div className="w-12 h-12 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Analytics Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recruiting Funnel</CardTitle>
            <CardDescription>Visual summary of candidate drop-off stages across all open jobs.</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                <Bar dataKey="count" fill="url(#funnelGradient)" radius={[4, 4, 0, 0]} />
                <defs>
                  <linearGradient id="funnelGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#4f5bf6" />
                    <stop offset="100%" stopColor="#312e81" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Interview Distribution</CardTitle>
            <CardDescription>Number of technical and conversational interviews scheduled this week.</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                <Line type="monotone" dataKey="interviews" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recruiter Activity and Pipeline Status */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Pipeline Table */}
        <Card className="xl:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Recent Candidates</CardTitle>
              <CardDescription>Pipeline screening summary for incoming applicant resumes.</CardDescription>
            </div>
            <Badge variant="primary" size="sm">Live Feed</Badge>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Candidate</TableHead>
                  <TableHead>Target Job Role</TableHead>
                  <TableHead>AI Match</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mockCandidates.slice(0, 4).map((cand) => (
                  <TableRow key={cand.id}>
                    <TableCell className="font-semibold text-white">{cand.name}</TableCell>
                    <TableCell>{cand.role}</TableCell>
                    <TableCell>
                      <span className={`font-semibold ${
                        cand.matchScore >= 90 ? 'text-emerald-400' :
                        cand.matchScore >= 80 ? 'text-blue-400' : 'text-amber-400'
                      }`}>
                        {cand.matchScore}%
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          cand.status === 'Interviewing' ? 'warning' :
                          cand.status === 'Offered' ? 'success' :
                          cand.status === 'Rejected' ? 'danger' :
                          cand.status === 'AI Screened' ? 'primary' : 'gray'
                        }
                      >
                        {cand.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* AI Action Items List */}
        <Card>
          <CardHeader>
            <CardTitle>AI Action Insights</CardTitle>
            <CardDescription>Generated recommendation metrics based on system logs.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4">
              <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 flex gap-3">
                <div className="shrink-0 text-amber-400 mt-0.5">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Review Required</h4>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">Sarah Connor scored exceptionally high (94%) on TypeScript skills. Consider fast-tracking to panel interview.</p>
                </div>
              </div>

              <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 flex gap-3">
                <div className="shrink-0 text-emerald-400 mt-0.5">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Index Ready</h4>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">Faiss RAG vectors successfully updated for "AI / Machine Learning Engineer" job resources. Context is live.</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
export default DashboardPage;
