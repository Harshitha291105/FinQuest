import { useState, useEffect } from 'react'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { Search } from '@/components/search'
import { ThemeSwitch } from '@/components/theme-switch'
import { ConfigDrawer } from '@/components/config-drawer'
import { ForecastCard } from './components/forecast-card'
import { RecommendationsList } from './components/recommendations-list'
import { fetchForecastData, type ForecastData } from '@/lib/api'

export function Forecast() {
  const [data, setData] = useState<ForecastData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadForecastData = async () => {
      try {
        setLoading(true)
        const forecastData = await fetchForecastData()
        setData(forecastData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch forecast data')
      } finally {
        setLoading(false)
      }
    }

    loadForecastData()
  }, [])

  return (
    <>
      <Header fixed>
        <Search />
        <div className='ms-auto flex items-center space-x-4'>
          <ThemeSwitch />
          <ConfigDrawer />
        </div>
      </Header>

      <Main>
        <div className='mb-6 flex flex-wrap items-center justify-between space-y-2'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>Analysis & Forecasting</h2>
            <p className='text-muted-foreground'>
              Track your spending patterns and get AI-powered recommendations for better financial management.
            </p>
          </div>
        </div>

        {loading && (
          <div className="flex items-center justify-center h-64">
            <div className="text-lg">Loading forecast data...</div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-64">
            <div className="text-red-600">Error: {error}</div>
          </div>
        )}

        {data && (
          <div className="space-y-6">
            {/* Forecast Cards Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {Object.entries(data.forecast).map(([category, forecastData]) => (
                <ForecastCard
                  key={category}
                  category={category}
                  spent={forecastData.spent_so_far}
                  budget={forecastData.budget}
                  projected={forecastData.projected_end_of_month}
                  status={forecastData.status}
                />
              ))}
            </div>

            {/* Recommendations */}
            <RecommendationsList recommendations={data.reccs} />
          </div>
        )}
      </Main>
    </>
  )
}