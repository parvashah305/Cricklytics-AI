import cors from 'cors'
import express from 'express'
import helmet from 'helmet'
import morgan from 'morgan'

import { matchesRouter } from './routes/matches.js'

const app = express()

app.use(helmet())
app.use(cors())
app.use(express.json())
app.use(morgan('dev'))

app.get('/health', (_req, res) => {
  res.json({ success: true, data: { status: 'ok' }, meta: { timestamp: new Date() } })
})

app.use('/api/matches', matchesRouter)

app.use((err, _req, res, _next) => {
  res.status(500).json({
    success: false,
    error: { code: 'INTERNAL_ERROR', message: err.message || 'Unexpected server error' }
  })
})

export { app }
