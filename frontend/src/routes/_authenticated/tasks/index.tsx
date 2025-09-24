import z from 'zod'
import { createFileRoute } from '@tanstack/react-router'
import { Transactions } from '@/features/transactions'

const transactionSearchSchema = z.object({
  page: z.number().optional().catch(1),
  pageSize: z.number().optional().catch(10),
  category: z.string().optional().catch(''),
  merchant: z.string().optional().catch(''),
  dateFrom: z.string().optional().catch(''),
  dateTo: z.string().optional().catch(''),
})

export const Route = createFileRoute('/_authenticated/tasks/')({
  validateSearch: transactionSearchSchema,
  component: Transactions,
})
