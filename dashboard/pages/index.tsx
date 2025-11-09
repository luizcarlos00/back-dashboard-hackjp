import { useEffect, useState, useMemo } from 'react';
import Layout from '../components/Layout';
import DashboardStats from '../components/DashboardStats';
import Filters from '../components/Filters';
import StudentCard from '../components/StudentCard';
import StudentDetailModal from '../components/StudentDetailModal';
import DifficultyDistribution from '../components/charts/DifficultyDistribution';
import ProgressOverview from '../components/charts/ProgressOverview';
import ContentTypeChart from '../components/charts/ContentTypeChart';
import { Student, Filters as FiltersType, SortConfig } from '../types';
import { getStudentStats } from '../utils/mockData';
import { ArrowUpDown, Loader } from 'lucide-react';

const initialFilters: FiltersType = {
  search: '',
  ageRange: [10, 30],
  education: 'Todos',
  difficulty: 'Todos',
  contentType: 'todos'
};

export default function Home() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<FiltersType>(initialFilters);
  const [sortConfig, setSortConfig] = useState<SortConfig>({ field: 'nome', direction: 'asc' });
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    // Load students data from backend API
    // Use proxy configured in next.config.js or direct localhost for development
    const API_URL = typeof window !== 'undefined' && window.location.hostname === 'localhost'
      ? ''  // Development - browser to localhost
      : '';  // Production - use proxy from next.config.js
    
    fetch(`${API_URL}/api/v1/dashboard-frontend/students`)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log('✅ Students loaded from backend:', data.length);
        setStudents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('❌ Error loading students from backend:', err);
        console.log('⚠️ Falling back to mock data (40 students)...');
        // Fallback to mock data if backend is not available
        import('../utils/mockData').then(({ generateStudents }) => {
          setStudents(generateStudents(40));
          setLoading(false);
        });
      });
  }, []);

  const filteredStudents = useMemo(() => {
    let filtered = students.filter(student => {
      if (filters.search && !student.nome.toLowerCase().includes(filters.search.toLowerCase())) {
        return false;
      }

      if (student.idade < filters.ageRange[0] || student.idade > filters.ageRange[1]) {
        return false;
      }

      if (filters.education !== 'Todos' && student.escolaridade !== filters.education) {
        return false;
      }

      if (filters.contentType !== 'todos') {
        const hasContentType = student.conteudos.some(c => c.tipo === filters.contentType);
        if (!hasContentType) return false;
      }

      if (filters.difficulty !== 'Todos') {
        const hasDifficulty = student.conteudos.some(c => c.dificuldade === filters.difficulty);
        if (!hasDifficulty) return false;
      }

      return true;
    });

    filtered.sort((a, b) => {
      let aValue: any;
      let bValue: any;

      if (sortConfig.field === 'completionRate') {
        aValue = getStudentStats(a).completionRate;
        bValue = getStudentStats(b).completionRate;
      } else {
        aValue = a[sortConfig.field];
        bValue = b[sortConfig.field];
      }

      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortConfig.direction === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortConfig.direction === 'asc' 
          ? aValue - bValue
          : bValue - aValue;
      }

      return 0;
    });

    return filtered;
  }, [students, filters, sortConfig]);

  const handleOpenModal = (student: Student) => {
    setSelectedStudent(student);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setTimeout(() => setSelectedStudent(null), 300);
  };

  const handleResetFilters = () => {
    setFilters(initialFilters);
  };

  const handleSort = (field: SortConfig['field']) => {
    setSortConfig(prev => ({
      field,
      direction: prev.field === field && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  if (loading) {
    return (
      <Layout title="Dashboard - Carregando...">
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader className="w-12 h-12 text-indigo-600 dark:text-indigo-400 animate-spin mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">Carregando dados...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Dashboard Estudantil">
      {/* Stats Overview */}
      <DashboardStats students={students} />

      {/* Filters */}
      <Filters 
        filters={filters} 
        onFiltersChange={setFilters}
        onReset={handleResetFilters}
      />

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <DifficultyDistribution students={filteredStudents} />
        <ContentTypeChart students={filteredStudents} />
      </div>

      <div className="mb-6">
        <ProgressOverview students={filteredStudents} />
      </div>

      {/* Sort Controls */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-6">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-2">
            <ArrowUpDown className="w-5 h-5 text-gray-500" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Ordenar por:
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {[
              { label: 'Nome', field: 'nome' as const },
              { label: 'Idade', field: 'idade' as const },
              { label: 'Escolaridade', field: 'escolaridade' as const },
              { label: 'Taxa de Conclusão', field: 'completionRate' as const },
            ].map(({ label, field }) => (
              <button
                key={field}
                onClick={() => handleSort(field)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  sortConfig.field === field
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {label}
                {sortConfig.field === field && (
                  <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Students Grid */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Estudantes
            <span className="ml-2 text-lg font-normal text-gray-500 dark:text-gray-400">
              ({filteredStudents.length})
            </span>
          </h2>
        </div>

        {filteredStudents.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-12 text-center">
            <p className="text-gray-500 dark:text-gray-400">
              Nenhum estudante encontrado com os filtros aplicados.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredStudents.map(student => (
              <StudentCard
                key={student.id}
                student={student}
                onClick={() => handleOpenModal(student)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Student Detail Modal */}
      <StudentDetailModal
        student={selectedStudent}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </Layout>
  );
}

