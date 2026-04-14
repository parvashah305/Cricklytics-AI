import dotenv from 'dotenv'
import http from 'node:http'

import { Server as SocketServer } from 'socket.io'

import { app } from './app.js'
import { connectMongo } from './db/connectMongo.js'

dotenv.config()

const port = Number(process.env.PORT || 4000)
const server = http.createServer(app)
const io = new SocketServer(server, {
  cors: { origin: '*' }
})

io.on('connection', (socket) => {
  socket.on('match:subscribe', ({ match_id: matchId }) => {
    if (!matchId) return
    socket.join(`match:${matchId}`)
  })

  socket.on('match:unsubscribe', ({ match_id: matchId }) => {
    if (!matchId) return
    socket.leave(`match:${matchId}`)
  })
})

async function startServer() {
  await connectMongo()
  server.listen(port, () => {
    process.stdout.write(`Cricklytics backend listening on ${port}\n`)
  })
}

startServer().catch((error) => {
  process.stderr.write(`Startup failed: ${error.message}\n`)
  process.exit(1)
})
