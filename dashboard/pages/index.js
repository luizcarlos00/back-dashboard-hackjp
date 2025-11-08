import Head from 'next/head'
import { useEffect, useMemo, useState } from 'react'
import dynamic from 'next/dynamic'
import SmallCharts from '../components/SmallCharts'
// manter Charts available but load dynamically if still used elsewhere
const Charts = dynamic(() => import('../components/Charts'), { ssr: false })

function SummaryCards({ items, metric = 'videos' }) {
  // metric is one of 'videos' | 'atividades' | 'exercicios'
  const total = items.length
  const sum = items.reduce((s, it) => s + (Number(it[metric]) || 0), 0)
  const avg = total ? Math.round(sum / total) : 0
  return (
    <div style={{display: 'flex', gap: '1rem', marginBottom: '1rem'}}>
      <div style={{flex: 1, padding: '1rem', background: '#f5f5f5', borderRadius: 6}}>
        <div style={{fontSize: 12, color: '#666'}}>Total de registros</div>
        <div style={{fontSize: 24, fontWeight: 'bold'}}>{total}</div>
      </div>
      <div style={{flex: 1, padding: '1rem', background: '#f5f5f5', borderRadius: 6}}>
        <div style={{fontSize: 12, color: '#666'}}>{`Soma de ${metric}`}</div>
        <div style={{fontSize: 24, fontWeight: 'bold'}}>{sum}</div>
      </div>
      <div style={{flex: 1, padding: '1rem', background: '#f5f5f5', borderRadius: 6}}>
        <div style={{fontSize: 12, color: '#666'}}>Média</div>
        <div style={{fontSize: 24, fontWeight: 'bold'}}>{avg}</div>
      </div>
    </div>
  )
}

function BarChart({ items }) {
  // usar 'videos' como altura das barras
  const max = Math.max(1, ...items.map(i => Number(i.videos) || 0))
  return (
    <div style={{display: 'flex', gap: 8, alignItems: 'end', padding: '1rem 0'}}>
      {items.map(it => (
        <div key={it.id} title={`${it.name}: ${it.videos}`} style={{flex: 1}}>
          <div style={{height: 6, background: '#ddd', borderRadius: 4, overflow: 'hidden'}}>
            <div style={{width: `${((Number(it.videos) || 0) / max) * 100}%`, height: 6, background: '#4f46e5'}} />
          </div>
          <div style={{fontSize: 11, marginTop: 6, textAlign: 'center'}}>{it.name}</div>
        </div>
      ))}
    </div>
  )
}

export default function Home() {
  const [data, setData] = useState(null)
  const [query, setQuery] = useState('')
  const [metric, setMetric] = useState('videos')
  const [sortKey, setSortKey] = useState('id')
  const [sortDir, setSortDir] = useState('asc')

  useEffect(() => {
    let mounted = true
    fetch('/data.json')
      .then(r => r.json())
      .then(json => { if (mounted) setData(json) })
      .catch(err => { console.error('Erro ao carregar data.json', err); if (mounted) setData([]) })
    return () => { mounted = false }
  }, [])

  const filtered = useMemo(() => {
    if (!data) return []
    const q = query.trim().toLowerCase()
    let list = data.filter(it => {
      if (!q) return true
      // search in name and numeric fields
      return (it.name && it.name.toLowerCase().includes(q)) || String(it.videos).includes(q) || String(it.atividades).includes(q) || String(it.exercicios).includes(q)
    })
    list = list.slice().sort((a, b) => {
      const av = a[sortKey]
      const bv = b[sortKey]
      if (av == null) return 1
      if (bv == null) return -1
      if (typeof av === 'number' && typeof bv === 'number') return sortDir === 'asc' ? av - bv : bv - av
      return sortDir === 'asc' ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av))
    })
    return list
  }, [data, query, sortKey, sortDir])

  function toggleSort(key) {
    if (sortKey === key) setSortDir(d => (d === 'asc' ? 'desc' : 'asc'))
    else { setSortKey(key); setSortDir('asc') }
  }

  return (
    <>
      <Head>
        <title>Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <main style={{fontFamily: 'Arial, sans-serif', padding: '2rem'}}>
        <h1>Dashboard Interativo</h1>
        <p>Dados carregados de <code>/public/data.json</code>. Edite este arquivo para testar outros conjuntos.</p>

        {!data ? (
          <div>Carregando dados...</div>
        ) : (
          <>
            <SummaryCards items={data} metric={metric} />

            <div style={{display: 'flex', gap: 12, marginBottom: 12, alignItems: 'center'}}>
              <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Pesquisar por nome ou número" style={{flex: 1, padding: '8px 10px', borderRadius: 6, border: '1px solid #ddd'}} />
              <select value={metric} onChange={e => setMetric(e.target.value)} style={{padding: '8px', borderRadius: 6, border: '1px solid #ddd'}}>
                <option value="videos">Vídeos</option>
                <option value="atividades">Atividades</option>
                <option value="exercicios">Exercícios</option>
              </select>
              <div style={{display: 'flex', gap: 8}}>
                <button onClick={() => { setQuery(''); setSortKey('id'); setSortDir('asc'); setMetric('videos') }} style={{padding: '8px 12px'}}>Reset</button>
              </div>
            </div>

            <div style={{padding: 12, background: '#fff', borderRadius: 6, border: '1px solid #eee', marginBottom: 16}}>
              <h3 style={{marginTop: 0}}>Gráfico (barras proporcionais)</h3>
              {/* mostra vários mini-gráficos compactos (evita scroll) */}
              <SmallCharts data={filtered} metric={metric} limit={12} />
            </div>

            <div style={{overflowX: 'auto', background: '#fff', borderRadius: 6, border: '1px solid #eee'}}>
              <table style={{width: '100%', borderCollapse: 'collapse'}}>
                <thead>
                  <tr style={{textAlign: 'left', borderBottom: '1px solid #f0f0f0'}}>
                    <th style={{padding: '8px 12px', cursor: 'pointer'}} onClick={() => toggleSort('id')}>ID {sortKey === 'id' ? (sortDir === 'asc' ? '▲' : '▼') : ''}</th>
                    <th style={{padding: '8px 12px', cursor: 'pointer'}} onClick={() => toggleSort('name')}>Nome {sortKey === 'name' ? (sortDir === 'asc' ? '▲' : '▼') : ''}</th>
                    <th style={{padding: '8px 12px', cursor: 'pointer'}} onClick={() => toggleSort('videos')}>Vídeos {sortKey === 'videos' ? (sortDir === 'asc' ? '▲' : '▼') : ''}</th>
                    <th style={{padding: '8px 12px', cursor: 'pointer'}} onClick={() => toggleSort('atividades')}>Atividades {sortKey === 'atividades' ? (sortDir === 'asc' ? '▲' : '▼') : ''}</th>
                    <th style={{padding: '8px 12px', cursor: 'pointer'}} onClick={() => toggleSort('exercicios')}>Exercícios {sortKey === 'exercicios' ? (sortDir === 'asc' ? '▲' : '▼') : ''}</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map(it => (
                    <tr key={it.id} style={{borderBottom: '1px solid #f7f7f7'}}>
                      <td style={{padding: '8px 12px'}}>{it.id}</td>
                      <td style={{padding: '8px 12px'}}>{it.name}</td>
                      <td style={{padding: '8px 12px'}}>{it.videos}</td>
                      <td style={{padding: '8px 12px'}}>{it.atividades}</td>
                      <td style={{padding: '8px 12px'}}>{it.exercicios}</td>
                    </tr>
                  ))}
                  {filtered.length === 0 && (
                    <tr><td colSpan={5} style={{padding: 12}}>Nenhum registro encontrado.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
    </>
  )
}
