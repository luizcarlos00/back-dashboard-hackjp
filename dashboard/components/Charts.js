import { useMemo } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar, Doughnut } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend)

export default function Charts({ data }) {
  // data: array of { id, name, videos, atividades, exercicios }
  const top = useMemo(() => {
    const arr = Array.isArray(data) ? data : (data ? Object.values(data) : [])
    return arr.slice().sort((a, b) => (b.videos || 0) - (a.videos || 0)).slice(0, 8)
  }, [data]);

  const barData = useMemo(() => ({
    labels: top.map(i => i.name),
    datasets: [
      {
        label: 'Vídeos vistos',
        data: top.map(i => Number(i.videos) || 0),
        backgroundColor: 'rgba(79,70,229,0.8)'
      }
    ]
  }), [top]);

  const totals = useMemo(() => {
    const t = { videos: 0, atividades: 0, exercicios: 0 };
    const arr = Array.isArray(data) ? data : (data ? Object.values(data) : []);
    arr.forEach(i => {
      t.videos += Number(i.videos) || 0;
      t.atividades += Number(i.atividades) || 0;
      t.exercicios += Number(i.exercicios) || 0;
    });
    return t;
  }, [data]);

  const doughnutData = useMemo(() => ({
    labels: ['Vídeos', 'Atividades', 'Exercícios'],
    datasets: [
      {
        data: [totals.videos, totals.atividades, totals.exercicios],
        backgroundColor: ['#4f46e5', '#06b6d4', '#f59e0b']
      }
    ]
  }), [totals])

  return (
    <div style={{display: 'grid', gridTemplateColumns: '1fr 320px', gap: 16}}>
      <div style={{padding: 12, background: '#fff', borderRadius: 8, border: '1px solid #eee'}}>
  <h4 style={{marginTop: 0}}>Top {top.length} por vídeos</h4>
  {/* diminuir altura para evitar scroll da página */}
  <Bar data={barData} options={{responsive: true, maintainAspectRatio: false, plugins: {legend: {display: false}}}} height={140} />
      </div>

      <div style={{padding: 12, background: '#fff', borderRadius: 8, border: '1px solid #eee'}}>
        <h4 style={{marginTop: 0}}>Distribuição total</h4>
        <div style={{height: 140}}>
          <Doughnut data={doughnutData} options={{responsive: true, maintainAspectRatio: false, plugins: {legend: {position: 'bottom'}}}} />
        </div>
      </div>
    </div>
  )
}
