import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { X, GraduationCap, Clock, Video, FileText, ClipboardList, CheckCircle2, Circle } from 'lucide-react';
import { Student, Content } from '../types';
import { getStudentStats } from '../utils/mockData';

interface StudentDetailModalProps {
  student: Student | null;
  isOpen: boolean;
  onClose: () => void;
}

function ContentIcon({ tipo }: { tipo: Content['tipo'] }) {
  switch (tipo) {
    case 'video':
      return <Video className="w-4 h-4" />;
    case 'atividade':
      return <FileText className="w-4 h-4" />;
    case 'exercicio':
      return <ClipboardList className="w-4 h-4" />;
  }
}

function DifficultyBadge({ dificuldade }: { dificuldade: Content['dificuldade'] }) {
  const colors = {
    'Fácil': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    'Médio': 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
    'Difícil': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[dificuldade]}`}>
      {dificuldade}
    </span>
  );
}

export default function StudentDetailModal({ student, isOpen, onClose }: StudentDetailModalProps) {
  if (!student) return null;

  const stats = getStudentStats(student);
  
  // Group contents by type
  const contentsByType = {
    video: student.conteudos.filter(c => c.tipo === 'video'),
    atividade: student.conteudos.filter(c => c.tipo === 'atividade'),
    exercicio: student.conteudos.filter(c => c.tipo === 'exercicio')
  };

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25 dark:bg-opacity-50" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-3xl transform overflow-hidden rounded-2xl 
                                       bg-white dark:bg-gray-800 text-left align-middle shadow-xl transition-all">
                {/* Header */}
                <div className="flex items-start justify-between p-6 border-b border-gray-200 dark:border-gray-700">
                  <div>
                    <Dialog.Title
                      as="h3"
                      className="text-2xl font-semibold text-gray-900 dark:text-white mb-2"
                    >
                      {student.nome}
                    </Dialog.Title>
                    <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
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
                  <button
                    onClick={onClose}
                    className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-500" />
                  </button>
                </div>

                {/* Stats Overview */}
                <div className="p-6 bg-gray-50 dark:bg-gray-900">
                  <div className="grid grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-white dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                        {student.conteudos.length}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Total</div>
                    </div>
                    <div className="text-center p-3 bg-white dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {stats.completedCount}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Concluídos</div>
                    </div>
                    <div className="text-center p-3 bg-white dark:bg-gray-800 rounded-lg">
                      <div className={`text-2xl font-bold ${
                        stats.completionRate >= 70 ? 'text-green-600 dark:text-green-400' : 
                        stats.completionRate >= 40 ? 'text-amber-600 dark:text-amber-400' : 
                        'text-red-600 dark:text-red-400'
                      }`}>
                        {stats.completionRate}%
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Progresso</div>
                    </div>
                    <div className="text-center p-3 bg-white dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                        {student.conteudos.length - stats.completedCount}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Restantes</div>
                    </div>
                  </div>
                </div>

                {/* Content List */}
                <div className="p-6 max-h-96 overflow-y-auto">
                  <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Conteúdos
                  </h4>
                  
                  <div className="space-y-4">
                    {/* Videos */}
                    {contentsByType.video.length > 0 && (
                      <div>
                        <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                          <Video className="w-4 h-4" />
                          Vídeos ({contentsByType.video.length})
                        </h5>
                        <div className="space-y-2">
                          {contentsByType.video.map(content => (
                            <div
                              key={content.id}
                              className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
                            >
                              <div className="flex items-center gap-3 flex-1">
                                {content.concluido ? (
                                  <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0" />
                                ) : (
                                  <Circle className="w-5 h-5 text-gray-400 flex-shrink-0" />
                                )}
                                <span className={`text-sm ${
                                  content.concluido 
                                    ? 'text-gray-500 dark:text-gray-400 line-through' 
                                    : 'text-gray-900 dark:text-white'
                                }`}>
                                  {content.titulo}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <DifficultyBadge dificuldade={content.dificuldade} />
                                {content.dataInicio && (
                                  <span className="text-xs text-gray-500 dark:text-gray-400">
                                    {new Date(content.dataInicio).toLocaleDateString('pt-BR')}
                                  </span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Atividades */}
                    {contentsByType.atividade.length > 0 && (
                      <div>
                        <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                          <FileText className="w-4 h-4" />
                          Atividades ({contentsByType.atividade.length})
                        </h5>
                        <div className="space-y-2">
                          {contentsByType.atividade.map(content => (
                            <div
                              key={content.id}
                              className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
                            >
                              <div className="flex items-center gap-3 flex-1">
                                {content.concluido ? (
                                  <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0" />
                                ) : (
                                  <Circle className="w-5 h-5 text-gray-400 flex-shrink-0" />
                                )}
                                <span className={`text-sm ${
                                  content.concluido 
                                    ? 'text-gray-500 dark:text-gray-400 line-through' 
                                    : 'text-gray-900 dark:text-white'
                                }`}>
                                  {content.titulo}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <DifficultyBadge dificuldade={content.dificuldade} />
                                {content.dataInicio && (
                                  <span className="text-xs text-gray-500 dark:text-gray-400">
                                    {new Date(content.dataInicio).toLocaleDateString('pt-BR')}
                                  </span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Exercícios */}
                    {contentsByType.exercicio.length > 0 && (
                      <div>
                        <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                          <ClipboardList className="w-4 h-4" />
                          Exercícios ({contentsByType.exercicio.length})
                        </h5>
                        <div className="space-y-2">
                          {contentsByType.exercicio.map(content => (
                            <div
                              key={content.id}
                              className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
                            >
                              <div className="flex items-center gap-3 flex-1">
                                {content.concluido ? (
                                  <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0" />
                                ) : (
                                  <Circle className="w-5 h-5 text-gray-400 flex-shrink-0" />
                                )}
                                <span className={`text-sm ${
                                  content.concluido 
                                    ? 'text-gray-500 dark:text-gray-400 line-through' 
                                    : 'text-gray-900 dark:text-white'
                                }`}>
                                  {content.titulo}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <DifficultyBadge dificuldade={content.dificuldade} />
                                {content.dataInicio && (
                                  <span className="text-xs text-gray-500 dark:text-gray-400">
                                    {new Date(content.dataInicio).toLocaleDateString('pt-BR')}
                                  </span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}

