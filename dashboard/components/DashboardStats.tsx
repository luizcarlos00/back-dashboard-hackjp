import { Student } from '../types';
import { getStudentStats } from '../utils/mockData';
import { Users, Video, FileText, ClipboardList, TrendingUp, Award } from 'lucide-react';

interface DashboardStatsProps {
  students: Student[];
}

export default function DashboardStats({ students }: DashboardStatsProps) {
  // Calculate aggregate statistics
  const totalStudents = students.length;
  
  let totalVideos = 0;
  let totalAtividades = 0;
  let totalExercicios = 0;
  let totalCompleted = 0;
  let totalContent = 0;
  
  students.forEach(student => {
    const stats = getStudentStats(student);
    totalVideos += stats.totalVideos;
    totalAtividades += stats.totalAtividades;
    totalExercicios += stats.totalExercicios;
    totalCompleted += stats.completedCount;
    totalContent += student.conteudos.length;
  });
  
  const avgCompletionRate = totalContent > 0 
    ? Math.round((totalCompleted / totalContent) * 100) 
    : 0;
  
  const avgContentPerStudent = totalStudents > 0 
    ? Math.round(totalContent / totalStudents) 
    : 0;

  const stats = [
    {
      name: 'Total de Estudantes',
      value: totalStudents,
      icon: Users,
      color: 'text-indigo-600 dark:text-indigo-400',
      bgColor: 'bg-indigo-50 dark:bg-indigo-900/20',
    },
    {
      name: 'Vídeos Totais',
      value: totalVideos,
      icon: Video,
      color: 'text-purple-600 dark:text-purple-400',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
    },
    {
      name: 'Atividades Totais',
      value: totalAtividades,
      icon: FileText,
      color: 'text-cyan-600 dark:text-cyan-400',
      bgColor: 'bg-cyan-50 dark:bg-cyan-900/20',
    },
    {
      name: 'Exercícios Totais',
      value: totalExercicios,
      icon: ClipboardList,
      color: 'text-amber-600 dark:text-amber-400',
      bgColor: 'bg-amber-50 dark:bg-amber-900/20',
    },
    {
      name: 'Taxa de Conclusão Média',
      value: `${avgCompletionRate}%`,
      icon: TrendingUp,
      color: avgCompletionRate >= 70 ? 'text-green-600 dark:text-green-400' : 
             avgCompletionRate >= 40 ? 'text-amber-600 dark:text-amber-400' : 
             'text-red-600 dark:text-red-400',
      bgColor: avgCompletionRate >= 70 ? 'bg-green-50 dark:bg-green-900/20' : 
               avgCompletionRate >= 40 ? 'bg-amber-50 dark:bg-amber-900/20' : 
               'bg-red-50 dark:bg-red-900/20',
    },
    {
      name: 'Média de Conteúdos/Estudante',
      value: avgContentPerStudent,
      icon: Award,
      color: 'text-pink-600 dark:text-pink-400',
      bgColor: 'bg-pink-50 dark:bg-pink-900/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <div
            key={stat.name}
            className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 
                     p-5 hover:shadow-lg transition-shadow duration-200"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                  {stat.name}
                </p>
                <p className={`text-3xl font-bold ${stat.color}`}>
                  {stat.value}
                </p>
              </div>
              <div className={`${stat.bgColor} ${stat.color} p-3 rounded-lg`}>
                <Icon className="w-6 h-6" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

