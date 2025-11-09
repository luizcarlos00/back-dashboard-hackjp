import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Student } from '../../types';
import { getStudentStats } from '../../utils/mockData';

interface ProgressOverviewProps {
  students: Student[];
}

export default function ProgressOverview({ students }: ProgressOverviewProps) {
  // Get top 10 students by completion rate
  const topStudents = students
    .map(student => ({
      nome: student.nome.split(' ')[0], // First name only for readability
      ...getStudentStats(student)
    }))
    .sort((a, b) => b.completionRate - a.completionRate)
    .slice(0, 10);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Top 10 Estudantes por Taxa de Conclusão
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={topStudents}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
          <XAxis 
            dataKey="nome" 
            stroke="#9ca3af"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#9ca3af"
            style={{ fontSize: '12px' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'rgba(31, 41, 55, 0.9)', 
              border: 'none',
              borderRadius: '8px',
              color: '#fff'
            }}
            formatter={(value: number) => `${value}%`}
          />
          <Legend />
          <Bar 
            dataKey="completionRate" 
            name="Taxa de Conclusão (%)" 
            fill="#6366f1"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

