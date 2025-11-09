import { Student } from '../types';
import { getStudentStats } from '../utils/mockData';
import { GraduationCap, Clock, CheckCircle2 } from 'lucide-react';

interface StudentCardProps {
  student: Student;
  onClick: () => void;
}

export default function StudentCard({ student, onClick }: StudentCardProps) {
  const stats = getStudentStats(student);
  
  return (
    <div
      onClick={onClick}
      className="group bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 
                 p-5 cursor-pointer transition-all duration-200 
                 hover:shadow-lg hover:scale-[1.02] hover:border-indigo-300 dark:hover:border-indigo-600"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1 
                         group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
            {student.nome}
          </h3>
          <div className="flex items-center gap-3 text-sm text-gray-600 dark:text-gray-400">
            <span className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {student.idade} anos
            </span>
            <span className="flex items-center gap-1">
              <GraduationCap className="w-4 h-4" />
              {student.escolaridade}
            </span>
          </div>
        </div>
        
        <div className="flex flex-col items-end">
          <div className={`text-2xl font-bold ${
            stats.completionRate >= 70 ? 'text-green-600 dark:text-green-400' : 
            stats.completionRate >= 40 ? 'text-amber-600 dark:text-amber-400' : 
            'text-red-600 dark:text-red-400'
          }`}>
            {stats.completionRate}%
          </div>
          <span className="text-xs text-gray-500 dark:text-gray-400">conclusão</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div 
            className={`h-full transition-all duration-300 ${
              stats.completionRate >= 70 ? 'bg-green-500' : 
              stats.completionRate >= 40 ? 'bg-amber-500' : 
              'bg-red-500'
            }`}
            style={{ width: `${stats.completionRate}%` }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-3 gap-3">
        <div className="text-center p-2 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div className="text-lg font-semibold text-indigo-600 dark:text-indigo-400">
            {stats.totalVideos}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400">Vídeos</div>
        </div>
        <div className="text-center p-2 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div className="text-lg font-semibold text-cyan-600 dark:text-cyan-400">
            {stats.totalAtividades}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400">Atividades</div>
        </div>
        <div className="text-center p-2 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div className="text-lg font-semibold text-amber-600 dark:text-amber-400">
            {stats.totalExercicios}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400">Exercícios</div>
        </div>
      </div>

      {/* Completed Badge */}
      <div className="mt-3 flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
        <CheckCircle2 className="w-4 h-4 text-green-500" />
        <span>{stats.completedCount} de {student.conteudos.length} concluídos</span>
      </div>
    </div>
  );
}

