import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface ForecastCardProps {
  category: string
  spent: number
  budget: number
  projected: number
  status: string
}

// Simple progress bar component
function Progress({ value, className = '' }: { value: number; className?: string }) {
  return (
    <div className={`w-full bg-gray-200 rounded-full h-2 ${className}`}>
      <div 
        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
        style={{ width: `${Math.min(value, 100)}%` }}
      />
    </div>
  )
}

export function ForecastCard({ category, spent, budget, projected, status }: ForecastCardProps) {
  const spentPercentage = (spent / budget) * 100
  const projectedPercentage = (projected / budget) * 100

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium">{category}</CardTitle>
          <Badge variant={status === 'on track' ? 'default' : 'destructive'}>
            {status}
          </Badge>
        </div>
        <CardDescription>
          Budget: ${budget.toFixed(2)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-sm">
              <span>Spent so far</span>
              <span>${spent.toFixed(2)}</span>
            </div>
            <Progress value={spentPercentage} className="mt-1" />
          </div>
          
          <div>
            <div className="flex justify-between text-sm">
              <span>Projected end of month</span>
              <span className={projected > budget ? 'text-red-600' : 'text-green-600'}>
                ${projected.toFixed(2)}
              </span>
            </div>
            <Progress 
              value={projectedPercentage} 
              className="mt-1"
            />
          </div>
          
          {projected > budget && (
            <div className="text-sm text-red-600">
              Over budget by ${(projected - budget).toFixed(2)}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}