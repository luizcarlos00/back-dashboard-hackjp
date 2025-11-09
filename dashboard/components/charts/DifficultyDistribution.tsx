import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Student } from '../../types';

interface DifficultyDistributionProps {
  students: Student[];
}

const COLORS = {
  'Fácil': '#10b981',
  'Médio': '#f59e0b',
  'Difícil': '#ef4444'
};

export default function DifficultyDistribution({ students }: DifficultyDistributionProps) {
  // Count content by difficulty
  const difficultyCounts = {
    'Fácil': 0,
    'Médio': 0,
    'Difícil': 0
  };

  students.forEach(student => {
    student.conteudos.forEach(content => {
      difficultyCounts[content.dificuldade]++;
    });
  });

  const data = [
    { name: 'Fácil', value: difficultyCounts['Fácil'] },
    { name: 'Médio', value: difficultyCounts['Médio'] },
    { name: 'Difícil', value: difficultyCounts['Difícil'] },
  ].filter(item => item.value > 0);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Distribuição por Dificuldade
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS]} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'rgba(31, 41, 55, 0.9)', 
              border: 'none',
              borderRadius: '8px',
              color: '#fff'
            }} 
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

