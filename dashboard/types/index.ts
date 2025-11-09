export type ContentType = 'video' | 'atividade' | 'exercicio';
export type Difficulty = 'Fácil' | 'Médio' | 'Difícil';
export type EducationLevel = 'Fundamental' | 'Médio' | 'Superior';

export interface Content {
  id: string;
  tipo: ContentType;
  titulo: string;
  dificuldade: Difficulty;
  concluido: boolean;
  dataInicio?: string;
}

export interface Student {
  id: number;
  nome: string;
  idade: number;
  escolaridade: EducationLevel;
  conteudos: Content[];
}

export interface Filters {
  search: string;
  ageRange: [number, number];
  education: EducationLevel | 'Todos';
  difficulty: Difficulty | 'Todos';
  contentType: ContentType | 'todos';
}

export interface SortConfig {
  field: keyof Student | 'completionRate';
  direction: 'asc' | 'desc';
}

export interface StudentStats {
  totalVideos: number;
  totalAtividades: number;
  totalExercicios: number;
  completedCount: number;
  completionRate: number;
}

