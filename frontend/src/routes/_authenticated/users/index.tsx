import { createFileRoute } from '@tanstack/react-router'
import { Forecast } from '@/features/forecast'

export const Route = createFileRoute('/_authenticated/users/')({
  component: Forecast,
})
