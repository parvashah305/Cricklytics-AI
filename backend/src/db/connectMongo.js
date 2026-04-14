import mongoose from 'mongoose'

export async function connectMongo() {
  const mongoUri = process.env.MONGO_URI

  if (!mongoUri) {
    throw new Error('MONGO_URI is missing. Add it to backend/.env')
  }

  await mongoose.connect(mongoUri, {
    serverSelectionTimeoutMS: 10000
  })
}
