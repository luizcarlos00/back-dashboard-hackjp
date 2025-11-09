import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Student } from '../../types';

interface ContentTypeChartProps {
  students: Student[];
}

export default function ContentTypeChart({ students }: ContentTypeChartProps) {
  // Count content by type
  const typeCounts = {
    video: 0,
    atividade: 0,
    exercicio: 0
  };

  students.forEach(student => {
    student.conteudos.forEach(content => {
      typeCounts[content.tipo]++;
    });
  });

  const data = [
    { tipo: 'Vídeos', total: typeCounts.video, color: '#6366f1' },
    { tipo: 'Atividades', total: typeCounts.atividade, color: '#06b6d4' },
    { tipo: 'Exercícios', total: typeCounts.exercicio, color: '#f59e0b' },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Conteúdos por Tipo
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
          <XAxis 
            dataKey="tipo" 
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
          />
          <Legend />
          <Bar 
            dataKey="total" 
            name="Total de Conteúdos"
            fill="#6366f1"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

