import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface RecommendationsListProps {
  recommendations: string[]
}

export function RecommendationsList({ recommendations }: RecommendationsListProps) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>AI Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No recommendations available.</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Recommendations</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {recommendations.map((recommendation, index) => (
            <Alert key={index}>
              <AlertDescription>{recommendation}</AlertDescription>
            </Alert>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}