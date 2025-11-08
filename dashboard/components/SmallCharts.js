// compact sparkline — pure SVG
function Sparkline({ values = [], width = 300, height = 48, color = '#4f46e5' }) {
  const pts = values.length ? values : [0]
  const max = Math.max(...pts, 1)
  const min = Math.min(...pts, 0)
  const range = max - min || 1
  const step = width / Math.max(1, pts.length - 1)
  const points = pts.map((v, i) => `${i * step},${height - ((v - min) / range) * height}`).join(' ')

  return (
    <svg width="100%" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none" style={{display: 'block'}}>
      <polyline fill="none" stroke={color} strokeWidth="2" points={points} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

// mini donut implemented with stacked SVG circles
function MiniDonut({ values = [], colors = ['#4f46e5', '#06b6d4', '#f59e0b'], size = 80, stroke = 12 }) {
  const total = Math.max(1, values.reduce((s, v) => s + (v || 0), 0))
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  let offset = 0

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <g transform={`rotate(-90 ${size / 2} ${size / 2})`}>
        {values.map((v, i) => {
          const dash = (v / total) * c
          const style = { stroke: colors[i % colors.length], strokeWidth: stroke, strokeLinecap: 'butt', fill: 'transparent', strokeDasharray: `${dash} ${c - dash}`, strokeDashoffset: -offset }
          offset += dash
          return <circle key={i} cx={size / 2} cy={size / 2} r={r} style={style} />
        })}
      </g>
      <text x="50%" y="50%" alignmentBaseline="middle" textAnchor="middle" fontSize={12} fill="#111">{total}</text>
    </svg>
  )
}

export default function SmallCharts({ data = [], metric = 'videos', limit = 12 }) {
  // data: array of { id, name, videos, atividades, exercicios }
  const arr = Array.isArray(data) ? data.slice(0, limit) : []
  const max = Math.max(1, ...arr.map(i => Number(i[metric]) || 0))

  // sparkline values: use the values of the current metric across the array
  const sparkValues = arr.map(i => Number(i[metric]) || 0)

  // totals for donut (videos, atividades, exercicios) across full data set
  const totalValues = (Array.isArray(data) ? data : []).reduce((t, it) => {
    t.videos += Number(it.videos) || 0
    t.atividades += Number(it.atividades) || 0
    t.exercicios += Number(it.exercicios) || 0
    return t
  }, { videos: 0, atividades: 0, exercicios: 0 })

  return (
    <div style={{display: 'grid', gap: 8}}>
      <div style={{display: 'flex', gap: 12, alignItems: 'center'}}>
        <div style={{flex: 1, padding: 8, background: '#fff', borderRadius: 8, border: '1px solid #eee'}}>
          <div style={{fontSize: 13, fontWeight: 700, marginBottom: 6}}>Tendência ({metric})</div>
          <Sparkline values={sparkValues} width={300} height={48} />
        </div>

        <div style={{width: 120, padding: 8, background: '#fff', borderRadius: 8, border: '1px solid #eee', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{fontSize: 13, fontWeight: 700, marginBottom: 6}}>Totais</div>
          <MiniDonut values={[totalValues.videos, totalValues.atividades, totalValues.exercicios]} />
        </div>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 8}}>
        {arr.map(item => {
          const value = Number(item[metric]) || 0
          const pct = Math.round((value / max) * 100)
          return (
            <div key={item.id} style={{padding: 8, background: '#fff', border: '1px solid #eee', borderRadius: 8, display: 'flex', gap: 8, alignItems: 'center'}}>
              <div style={{flex: 1}}>
                <div style={{fontSize: 12, fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}} title={item.name}>{item.name}</div>
                <div style={{height: 22, display: 'flex', alignItems: 'center', gap: 8, marginTop: 6}}>
                  <div style={{flex: 1, height: 8, background: '#f3f4f6', borderRadius: 8, overflow: 'hidden'}}>
                    <div style={{width: `${pct}%`, height: '100%', background: '#4f46e5'}} />
                  </div>
                  <div style={{width: 36, textAlign: 'right', fontSize: 12, color: '#333'}}>{value}</div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
