import { Student, Content, ContentType, Difficulty, EducationLevel } from '../types';

const firstNames = [
  'Ana', 'Bruno', 'Carla', 'Diego', 'Elisa', 'Felipe', 'Gabriela', 'Hugo',
  'Iara', 'João', 'Karla', 'Leandro', 'Mariana', 'Nicolas', 'Olívia', 'Pablo',
  'Queila', 'Rafael', 'Sofia', 'Thiago', 'Úrsula', 'Vitor', 'Wagner', 'Ximena',
  'Yara', 'Zeca', 'Andréa', 'Bernardo', 'Clara', 'Daniela', 'Eduardo', 'Fabiana',
  'Gustavo', 'Helena', 'Igor', 'Júlia', 'Kevin', 'Larissa', 'Mateus', 'Natália',
  'Olavo', 'Patrícia', 'Quirino', 'Rita', 'Samuel', 'Tatiana', 'Ubiratan', 'Vanessa'
];

const lastNames = [
  'Silva', 'Costa', 'Rocha', 'Santos', 'Pereira', 'Lima', 'Alves', 'Fernandes',
  'Moreira', 'Mendes', 'Nascimento', 'Ribeiro', 'Duarte', 'Castro', 'Gomes',
  'Martins', 'Sousa', 'Carvalho', 'Araújo', 'Pinto', 'Reis', 'Melo', 'Braga',
  'Lopes', 'Almeida', 'Barros', 'Faria', 'Viana', 'Freitas', 'Neves'
];

const contentTitles = {
  video: [
    'Introdução à Programação',
    'Estruturas de Dados Básicas',
    'Algoritmos de Ordenação',
    'Programação Orientada a Objetos',
    'Banco de Dados Relacional',
    'APIs REST e HTTP',
    'JavaScript Moderno',
    'React Fundamentos',
    'TypeScript Essencial',
    'Node.js Básico',
    'Python para Iniciantes',
    'Git e GitHub',
    'CSS Grid e Flexbox',
    'Responsividade Web',
    'Testes Automatizados'
  ],
  atividade: [
    'Exercício: Criar uma Lista',
    'Prática: Implementar Busca',
    'Atividade: Refatorar Código',
    'Desafio: Criar CRUD',
    'Projeto: Site Pessoal',
    'Lab: Consumir API',
    'Workshop: Design Patterns',
    'Exercício: Validação de Dados',
    'Prática: Componentes React',
    'Atividade: Estilização CSS',
    'Desafio: Formulário Completo',
    'Projeto: Dashboard',
    'Lab: Autenticação',
    'Workshop: Performance',
    'Exercício: Debugging'
  ],
  exercicio: [
    'Quiz: Conceitos Básicos',
    'Teste: Sintaxe JavaScript',
    'Avaliação: Lógica de Programação',
    'Quiz: HTML e CSS',
    'Teste: Funções e Escopo',
    'Avaliação: Arrays e Objetos',
    'Quiz: Async/Await',
    'Teste: Promises',
    'Avaliação: DOM Manipulation',
    'Quiz: React Hooks',
    'Teste: State Management',
    'Avaliação: TypeScript Types',
    'Quiz: SQL Queries',
    'Teste: REST APIs',
    'Avaliação: Git Commands'
  ]
};

function randomElement<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateContent(id: number): Content {
  const tipos: ContentType[] = ['video', 'atividade', 'exercicio'];
  const dificuldades: Difficulty[] = ['Fácil', 'Médio', 'Difícil'];
  
  const tipo = randomElement(tipos);
  const titulo = randomElement(contentTitles[tipo]);
  const dificuldade = randomElement(dificuldades);
  const concluido = Math.random() > 0.3; // 70% completion rate
  
  const content: Content = {
    id: `content-${id}`,
    tipo,
    titulo,
    dificuldade,
    concluido
  };
  
  if (concluido) {
    const daysAgo = randomInt(1, 90);
    const date = new Date();
    date.setDate(date.getDate() - daysAgo);
    content.dataInicio = date.toISOString().split('T')[0];
  }
  
  return content;
}

export function generateStudents(count: number = 40): Student[] {
  const students: Student[] = [];
  const educationLevels: EducationLevel[] = ['Fundamental', 'Médio', 'Superior'];
  
  for (let i = 1; i <= count; i++) {
    const nome = `${randomElement(firstNames)} ${randomElement(lastNames)}`;
    const escolaridade = randomElement(educationLevels);
    
    // Age ranges based on education level
    let idade: number;
    if (escolaridade === 'Fundamental') {
      idade = randomInt(10, 14);
    } else if (escolaridade === 'Médio') {
      idade = randomInt(15, 18);
    } else {
      idade = randomInt(18, 28);
    }
    
    const numConteudos = randomInt(5, 15);
    const conteudos: Content[] = [];
    
    for (let j = 1; j <= numConteudos; j++) {
      conteudos.push(generateContent(i * 100 + j));
    }
    
    students.push({
      id: i,
      nome,
      idade,
      escolaridade,
      conteudos
    });
  }
  
  return students;
}

export function getStudentStats(student: Student) {
  const totalVideos = student.conteudos.filter(c => c.tipo === 'video').length;
  const totalAtividades = student.conteudos.filter(c => c.tipo === 'atividade').length;
  const totalExercicios = student.conteudos.filter(c => c.tipo === 'exercicio').length;
  const completedCount = student.conteudos.filter(c => c.concluido).length;
  const completionRate = student.conteudos.length > 0 
    ? Math.round((completedCount / student.conteudos.length) * 100) 
    : 0;
  
  return {
    totalVideos,
    totalAtividades,
    totalExercicios,
    completedCount,
    completionRate
  };
}

