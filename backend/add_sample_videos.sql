-- Sample Videos for FeedBreak MVP
-- Run this in your Supabase SQL Editor after running schema.sql

-- Science Videos
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts) VALUES
('Como Funciona a Fotossíntese', 
 'Aprenda como as plantas convertem luz solar em energia através da fotossíntese.',
 'https://www.youtube.com/watch?v=example1',
 'https://img.youtube.com/vi/example1/maxresdefault.jpg',
 180,
 'ciencias',
 1,
 ARRAY['biologia', 'plantas', 'natureza'],
 ARRAY['luz solar', 'clorofila', 'glicose', 'energia', 'dióxido de carbono', 'oxigênio']),

('O Ciclo da Água',
 'Entenda o ciclo hidrológico e como a água circula no planeta.',
 'https://www.youtube.com/watch?v=example2',
 'https://img.youtube.com/vi/example2/maxresdefault.jpg',
 150,
 'ciencias',
 1,
 ARRAY['geografia', 'água', 'meio ambiente'],
 ARRAY['evaporação', 'condensação', 'precipitação', 'infiltração']),

('Células: As Unidades da Vida',
 'Descubra como funcionam as células, os blocos fundamentais dos seres vivos.',
 'https://www.youtube.com/watch?v=example3',
 'https://img.youtube.com/vi/example3/maxresdefault.jpg',
 200,
 'ciencias',
 2,
 ARRAY['biologia', 'célula', 'vida'],
 ARRAY['membrana', 'núcleo', 'citoplasma', 'organelas', 'DNA']);

-- Technology Videos
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts) VALUES
('Introdução à Programação',
 'Os conceitos básicos de programação e como computadores executam código.',
 'https://www.youtube.com/watch?v=example4',
 'https://img.youtube.com/vi/example4/maxresdefault.jpg',
 240,
 'tecnologia',
 2,
 ARRAY['programação', 'código', 'computação'],
 ARRAY['algoritmo', 'variáveis', 'loops', 'condicionais', 'funções']),

('Como Funciona a Internet',
 'Explore como a internet conecta o mundo inteiro.',
 'https://www.youtube.com/watch?v=example5',
 'https://img.youtube.com/vi/example5/maxresdefault.jpg',
 180,
 'tecnologia',
 1,
 ARRAY['internet', 'web', 'redes'],
 ARRAY['servidor', 'cliente', 'protocolo', 'TCP/IP', 'dados']),

('Inteligência Artificial Básica',
 'O que é IA e como máquinas podem aprender.',
 'https://www.youtube.com/watch?v=example6',
 'https://img.youtube.com/vi/example6/maxresdefault.jpg',
 220,
 'tecnologia',
 3,
 ARRAY['IA', 'machine learning', 'tecnologia'],
 ARRAY['aprendizado', 'dados', 'algoritmos', 'redes neurais', 'padrões']);

-- Math Videos
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts) VALUES
('Teorema de Pitágoras Explicado',
 'Aprenda o famoso teorema e suas aplicações práticas.',
 'https://www.youtube.com/watch?v=example7',
 'https://img.youtube.com/vi/example7/maxresdefault.jpg',
 160,
 'matematica',
 2,
 ARRAY['geometria', 'triângulos', 'teorema'],
 ARRAY['catetos', 'hipotenusa', 'quadrados', 'triângulo retângulo']),

('Frações na Prática',
 'Entenda frações e como usá-las no dia a dia.',
 'https://www.youtube.com/watch?v=example8',
 'https://img.youtube.com/vi/example8/maxresdefault.jpg',
 140,
 'matematica',
 1,
 ARRAY['matemática básica', 'frações', 'números'],
 ARRAY['numerador', 'denominador', 'simplificação', 'equivalência']),

('Probabilidade e Estatística Básica',
 'Conceitos fundamentais de probabilidade aplicados ao mundo real.',
 'https://www.youtube.com/watch?v=example9',
 'https://img.youtube.com/vi/example9/maxresdefault.jpg',
 190,
 'matematica',
 2,
 ARRAY['estatística', 'probabilidade', 'dados'],
 ARRAY['chance', 'média', 'porcentagem', 'eventos', 'amostra']);

-- History Videos
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts) VALUES
('A Revolução Industrial',
 'Como a industrialização mudou o mundo no século XVIII.',
 'https://www.youtube.com/watch?v=example10',
 'https://img.youtube.com/vi/example10/maxresdefault.jpg',
 210,
 'historia',
 2,
 ARRAY['história', 'industrialização', 'sociedade'],
 ARRAY['máquinas', 'fábricas', 'vapor', 'urbanização', 'trabalho']),

('Descobrimento do Brasil',
 'A chegada dos portugueses ao Brasil em 1500.',
 'https://www.youtube.com/watch?v=example11',
 'https://img.youtube.com/vi/example11/maxresdefault.jpg',
 170,
 'historia',
 1,
 ARRAY['brasil', 'história', 'descobrimento'],
 ARRAY['Portugal', 'Pedro Álvares Cabral', 'colonização', 'indígenas']),

('Segunda Guerra Mundial - Resumo',
 'Os principais eventos da Segunda Guerra Mundial.',
 'https://www.youtube.com/watch?v=example12',
 'https://img.youtube.com/vi/example12/maxresdefault.jpg',
 250,
 'historia',
 3,
 ARRAY['guerra', 'história mundial', 'conflito'],
 ARRAY['nazismo', 'aliados', 'eixo', 'holocausto', 'batalhas']);

-- Language/Portuguese Videos
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts) VALUES
('Sujeito e Predicado',
 'Aprenda a identificar sujeito e predicado em frases.',
 'https://www.youtube.com/watch?v=example13',
 'https://img.youtube.com/vi/example13/maxresdefault.jpg',
 150,
 'portugues',
 1,
 ARRAY['gramática', 'português', 'sintaxe'],
 ARRAY['sujeito', 'predicado', 'verbo', 'análise sintática']),

('Figuras de Linguagem',
 'Metáfora, metonímia e outras figuras de linguagem.',
 'https://www.youtube.com/watch?v=example14',
 'https://img.youtube.com/vi/example14/maxresdefault.jpg',
 180,
 'portugues',
 2,
 ARRAY['literatura', 'linguagem', 'figuras'],
 ARRAY['metáfora', 'comparação', 'hipérbole', 'personificação']),

('Tempos Verbais',
 'Entenda passado, presente e futuro dos verbos.',
 'https://www.youtube.com/watch?v=example15',
 'https://img.youtube.com/vi/example15/maxresdefault.jpg',
 160,
 'portugues',
 1,
 ARRAY['verbos', 'gramática', 'conjugação'],
 ARRAY['pretérito', 'presente', 'futuro', 'modo', 'tempo']);

-- Geography Videos
INSERT INTO videos (title, description, url, thumbnail_url, duration_seconds, category, difficulty, keywords, expected_concepts) VALUES
('Os Continentes e Oceanos',
 'Conheça os continentes e oceanos do planeta Terra.',
 'https://www.youtube.com/watch?v=example16',
 'https://img.youtube.com/vi/example16/maxresdefault.jpg',
 130,
 'geografia',
 1,
 ARRAY['geografia física', 'mundo', 'continentes'],
 ARRAY['América', 'Europa', 'Ásia', 'África', 'Oceania', 'Antártida', 'oceanos']),

('Clima e Zonas Climáticas',
 'Aprenda sobre os diferentes tipos de clima no mundo.',
 'https://www.youtube.com/watch?v=example17',
 'https://img.youtube.com/vi/example17/maxresdefault.jpg',
 170,
 'geografia',
 2,
 ARRAY['clima', 'meteorologia', 'ambiente'],
 ARRAY['tropical', 'temperado', 'polar', 'desértico', 'temperatura', 'precipitação']);

-- Check inserted videos
SELECT 
    category,
    COUNT(*) as video_count
FROM videos
WHERE is_active = true
GROUP BY category
ORDER BY category;

