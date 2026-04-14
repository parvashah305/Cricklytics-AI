import { Router } from 'express'

const matchesRouter = Router()

matchesRouter.get('/', (_req, res) => {
  res.json({
    success: true,
    data: { matches: [] },
    meta: { timestamp: new Date() }
  })
})

matchesRouter.get('/:id', (req, res) => {
  res.json({
    success: true,
    data: {
      match_id: req.params.id,
      teams: { home: 'TBD', away: 'TBD' },
      scorecard: { innings1: { runs: 0, wickets: 0, overs: 0 } }
    },
    meta: { timestamp: new Date(), match_id: req.params.id }
  })
})

export { matchesRouter }
