import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { DollarSign, Save } from 'lucide-react'

interface BudgetConstraints {
  food: number
  travel: number
  shopping: number
  entertainment: number
  bills: number
  transport: number
}

export function BudgetForm() {
  const [budgets, setBudgets] = useState<BudgetConstraints>({
    food: 0,
    travel: 0,
    shopping: 0,
    entertainment: 0,
    bills: 0,
    transport: 0
  })

  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  // Load existing budget data on component mount
  useEffect(() => {
    loadBudgetData()
  }, [])

  const loadBudgetData = async () => {
    try {
      const response = await fetch('http://localhost:5000/budget')
      if (response.ok) {
        const data = await response.json()
        // Direct mapping - categories are now identical
        setBudgets({
          food: data.Food || 0,
          travel: data.Travel || 0,
          shopping: data.Shopping || 0,
          entertainment: data.Entertainment || 0,
          bills: data.Bills || 0,
          transport: data.Transport || 0
        })
      }
    } catch (error) {
      console.error('Error loading budget data:', error)
    }
  }

  const categories = [
    { key: 'food', label: 'Food & Dining', icon: '🍽️' },
    { key: 'travel', label: 'Travel', icon: '✈️' },
    { key: 'shopping', label: 'Shopping', icon: '🛍️' },
    { key: 'entertainment', label: 'Entertainment', icon: '🎬' },
    { key: 'bills', label: 'Bills & Utilities', icon: '💡' },
    { key: 'transport', label: 'Transportation', icon: '🚗' }
  ]

  const handleInputChange = (category: keyof BudgetConstraints, value: string) => {
    const numValue = parseFloat(value) || 0
    setBudgets(prev => ({
      ...prev,
      [category]: numValue
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      const response = await fetch('http://localhost:5000/budget', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(budgets)
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Budget saved:', result)
        setIsSubmitted(true)
        
        // Show success message for 3 seconds
        setTimeout(() => setIsSubmitted(false), 3000)
      } else {
        throw new Error('Failed to save budget')
      }
    } catch (error) {
      console.error('Error saving budgets:', error)
      alert('Error saving budget constraints. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const totalBudget = Object.values(budgets).reduce((sum, amount) => sum + amount, 0)

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight">Set Your Budget Constraints</h2>
        <p className="text-muted-foreground mt-2">
          Define your monthly spending limits for each category to get better financial insights.
        </p>
      </div>

      {isSubmitted && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
          <p className="text-green-800 font-medium">✅ Budget constraints saved successfully!</p>
          <p className="text-green-600 text-sm">Your budget data will be used in Analysis & Forecasting.</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {categories.map((category) => (
            <Card key={category.key} className="relative">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <span className="text-2xl">{category.icon}</span>
                  {category.label}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Label htmlFor={category.key}>Monthly Budget</Label>
                  <div className="relative">
                    <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id={category.key}
                      type="number"
                      min="0"
                      step="0.01"
                      placeholder="0.00"
                      value={budgets[category.key as keyof BudgetConstraints] || ''}
                      onChange={(e) => handleInputChange(category.key as keyof BudgetConstraints, e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5" />
              Total Monthly Budget
            </CardTitle>
            <CardDescription>
              Sum of all category budgets
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
              ${totalBudget.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-center">
          <Button 
            type="submit" 
            size="lg" 
            disabled={isLoading || totalBudget === 0}
            className="min-w-[200px]"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Saving...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Save Budget Constraints
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}