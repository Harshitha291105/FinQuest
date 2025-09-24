import { createFileRoute } from '@tanstack/react-router'
import { BudgetPlanning } from '@/features/budget'

export const Route = createFileRoute('/_authenticated/budget/')({
  component: BudgetPlanning,
})