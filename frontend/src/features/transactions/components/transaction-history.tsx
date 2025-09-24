import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CalendarDays, DollarSign, Building2, Tag } from 'lucide-react'

interface Transaction {
  transaction_id: string
  account_id: string
  amount: number
  merchant_name: string
  category: string[]
  date: string
}

interface TransactionResponse {
  transactions: Transaction[]
  error?: string
}

const categoryColors: Record<string, string> = {
  food: 'bg-green-100 text-green-800',
  transport: 'bg-blue-100 text-blue-800',
  shopping: 'bg-purple-100 text-purple-800',
  entertainment: 'bg-pink-100 text-pink-800',
  bills: 'bg-orange-100 text-orange-800',
  travel: 'bg-indigo-100 text-indigo-800',
  other: 'bg-gray-100 text-gray-800'
}

export function TransactionHistory() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setLoading(true)
        const response = await fetch('http://localhost:5000/transactions')
        const data: TransactionResponse = await response.json()
        
        if (response.ok) {
          setTransactions(data.transactions)
        } else {
          setError(data.error || 'Failed to fetch transactions')
        }
      } catch (err) {
        setError('Failed to connect to server')
      } finally {
        setLoading(false)
      }
    }

    fetchTransactions()
  }, [])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading transactions...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-red-600">
            <p className="font-medium">Error loading transactions</p>
            <p className="text-sm text-muted-foreground mt-1">{error}</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Transactions</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{transactions.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(transactions.reduce((sum, tx) => sum + tx.amount, 0))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Transactions</CardTitle>
          <CardDescription>
            Your recent spending activity from Plaid integration
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {transactions.map((transaction) => (
              <div
                key={transaction.transaction_id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <Building2 className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="font-medium">{transaction.merchant_name}</p>
                    <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                      <CalendarDays className="h-3 w-3" />
                      <span>{formatDate(transaction.date)}</span>
                    </div>
                  </div>
                </div>
                
                <div className="text-right space-y-1">
                  <div className="font-bold text-lg">
                    {formatCurrency(transaction.amount)}
                  </div>
                  <div className="flex items-center space-x-1">
                    <Tag className="h-3 w-3" />
                    {transaction.category.map((cat) => (
                      <Badge
                        key={cat}
                        variant="secondary"
                        className={categoryColors[cat.toLowerCase()] || categoryColors.other}
                      >
                        {cat}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}