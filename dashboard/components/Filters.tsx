import { Search, X } from 'lucide-react';
import { Filters as FiltersType, EducationLevel, Difficulty, ContentType } from '../types';

interface FiltersProps {
  filters: FiltersType;
  onFiltersChange: (filters: FiltersType) => void;
  onReset: () => void;
}

export default function Filters({ filters, onFiltersChange, onReset }: FiltersProps) {
  const hasActiveFilters = 
    filters.search !== '' || 
    filters.education !== 'Todos' || 
    filters.difficulty !== 'Todos' ||
    filters.contentType !== 'todos' ||
    filters.ageRange[0] !== 10 || 
    filters.ageRange[1] !== 30;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Filtros</h3>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 
                     hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors"
          >
            <X className="w-4 h-4" />
            Limpar filtros
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div className="lg:col-span-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Buscar por nome
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={filters.search}
              onChange={(e) => onFiltersChange({ ...filters, search: e.target.value })}
              placeholder="Digite o nome do estudante..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 
                       rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                       focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent
                       placeholder-gray-400 dark:placeholder-gray-500 transition-colors"
            />
          </div>
        </div>

        {/* Education Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Escolaridade
          </label>
          <select
            value={filters.education}
            onChange={(e) => onFiltersChange({ ...filters, education: e.target.value as EducationLevel | 'Todos' })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 
                     rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent
                     transition-colors"
          >
            <option value="Todos">Todos</option>
            <option value="Fundamental">Fundamental</option>
            <option value="Médio">Médio</option>
            <option value="Superior">Superior</option>
          </select>
        </div>

        {/* Content Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Tipo de Conteúdo
          </label>
          <select
            value={filters.contentType}
            onChange={(e) => onFiltersChange({ ...filters, contentType: e.target.value as ContentType | 'todos' })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 
                     rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent
                     transition-colors"
          >
            <option value="todos">Todos</option>
            <option value="video">Vídeos</option>
            <option value="atividade">Atividades</option>
            <option value="exercicio">Exercícios</option>
          </select>
        </div>

        {/* Difficulty */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Dificuldade
          </label>
          <select
            value={filters.difficulty}
            onChange={(e) => onFiltersChange({ ...filters, difficulty: e.target.value as Difficulty | 'Todos' })}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 
                     rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent
                     transition-colors"
          >
            <option value="Todos">Todos</option>
            <option value="Fácil">Fácil</option>
            <option value="Médio">Médio</option>
            <option value="Difícil">Difícil</option>
          </select>
        </div>

        {/* Age Range */}
        <div className="lg:col-span-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Faixa Etária: {filters.ageRange[0]} - {filters.ageRange[1]} anos
          </label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min="10"
              max="30"
              value={filters.ageRange[0]}
              onChange={(e) => {
                const min = parseInt(e.target.value);
                onFiltersChange({ 
                  ...filters, 
                  ageRange: [min, Math.max(min, filters.ageRange[1])]
                });
              }}
              className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-indigo-600"
            />
            <input
              type="range"
              min="10"
              max="30"
              value={filters.ageRange[1]}
              onChange={(e) => {
                const max = parseInt(e.target.value);
                onFiltersChange({ 
                  ...filters, 
                  ageRange: [Math.min(max, filters.ageRange[0]), max]
                });
              }}
              className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-indigo-600"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

