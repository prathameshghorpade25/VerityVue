import React, { useEffect, useState } from 'react'
import { apiBase } from './api'

export default function App() {
	const [claims, setClaims] = useState([])
	const [selected, setSelected] = useState(null)

	const refresh = () => {
		fetch(`${apiBase}/claims`).then(r => r.json()).then(setClaims).catch(() => setClaims([]))
	}

	useEffect(() => { refresh() }, [])

	return (
		<div style={{ fontFamily: 'sans-serif', padding: 16 }}>
			<h2>VerityVue — Stream</h2>
			<button onClick={refresh}>Refresh</button>
			<div style={{ display: 'flex', gap: 24, marginTop: 12 }}>
				<div style={{ width: 380 }}>
					{claims.map(c => (
						<div key={c.id} style={{ border: '1px solid #ccc', padding: 8, marginBottom: 8, cursor: 'pointer' }} onClick={() => setSelected(c.id)}>
							<div><b>{c.text || '(no text)'}</b></div>
							<div style={{ fontSize: 12, color: '#555' }}>{c.uploader} — {c.timestamp}</div>
							<div style={{ fontSize: 12 }}>Status: {c.status}</div>
						</div>
					))}
				</div>
				<div style={{ flex: 2 }}>
					{selected ? <ClaimDetail id={selected} /> : <div>Select an item</div>}
				</div>
				<div style={{ flex: 1 }}>
					<AgentLog />
				</div>
			</div>
		</div>
	)
}

function ClaimDetail({ id }) {
	const [data, setData] = useState(null)
	const [token, setToken] = useState('demo-mod-token')
	const [showHeatmap, setShowHeatmap] = useState(false)

	const load = async () => {
		const d = await (await fetch(`${apiBase}/claims/${id}`)).json()
		setData(d)
	}
	useEffect(() => { load() }, [id])

	if (!data) return <div>Loading…</div>

	const publish = async () => {
		await fetch(`${apiBase}/claims/${id}/publish`, { method: 'POST', headers: { 'Authorization': token } })
		await load()
	}
	const escalate = async () => {
		await fetch(`${apiBase}/claims/${id}/escalate`, { method: 'POST', headers: { 'Authorization': token } })
		await load()
	}

	const displayImage = () => {
		if (showHeatmap && (data.heatmaps || []).length > 0) return data.heatmaps[0]
		if ((data.frames || []).length > 0) return data.frames[0]
		return null
	}

	const imgSrc = displayImage() ? `${apiBase.replace(/\/$/, '')}/media/${displayImage().split('/media/')?.[1] || displayImage()}` : null

	return (
		<div>
			<h3>Claim {data.id}</h3>
			<div>Text: {data.text}</div>
			<div>Status: {data.status}</div>
			<div>Verdict: {data.verdict?.label} ({data.verdict?.confidence}%)</div>
			<div style={{ marginTop: 8 }}>
				<b>Evidence</b>
				<ul>
					{(data.evidence || []).map((e, i) => (
						<li key={i}><a href={e.path_or_url || e.url} target="_blank" rel="noreferrer">{e.title || e.path_or_url}</a> {e.score != null ? `— ${Math.round(e.score*100)}%` : ''}</li>
					))}
				</ul>
			</div>
			<div style={{ marginTop: 8 }}>
				<input value={token} onChange={e => setToken(e.target.value)} style={{ width: 240 }} placeholder="Moderator token" />
				<button onClick={publish} style={{ marginLeft: 8 }}>Publish</button>
				<button onClick={escalate} style={{ marginLeft: 8 }}>Escalate</button>
				<label style={{ marginLeft: 16 }}><input type="checkbox" checked={showHeatmap} onChange={e => setShowHeatmap(e.target.checked)} /> Heatmap</label>
			</div>
			{imgSrc ? (
				<div style={{ marginTop: 8 }}>
					<img alt="preview" src={imgSrc} style={{ maxWidth: '100%' }} />
				</div>
			) : null}
			{data.advisory_preview ? (
				<div style={{ marginTop: 8, padding: 8, border: '1px dashed #aaa' }}>
					<b>Advisory:</b> {data.advisory_preview}
				</div>
			) : null}
		</div>
	)
}

function AgentLog() {
	const [logs, setLogs] = useState([])
	useEffect(() => {
		const load = async () => {
			const data = await (await fetch(`${apiBase}/agent/logs`)).json()
			setLogs(data.slice(-50).reverse())
		}
		load()
		const id = setInterval(load, 3000)
		return () => clearInterval(id)
	}, [])
	return (
		<div>
			<h3>Agent Log</h3>
			<div style={{ maxHeight: 480, overflow: 'auto', fontSize: 12 }}>
				{logs.map((l, i) => (
					<div key={i} style={{ borderBottom: '1px solid #eee', padding: 4 }}>
						<div>{l.timestamp}</div>
						<div><b>{l.event}</b> — {JSON.stringify(l.meta)}</div>
					</div>
				))}
			</div>
		</div>
	)
}
