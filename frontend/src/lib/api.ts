// API service for forecast data
const API_BASE_URL = 'http://127.0.0.1:5000'

export interface ForecastData {
  forecast: {
    [category: string]: {
      spent_so_far: number
      budget: number
      projected_end_of_month: number
      status: string
    }
  }
  reccs: string[]
}

export async function fetchForecastData(): Promise<ForecastData> {
  try {
    const response = await fetch(`${API_BASE_URL}/forecast`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error fetching forecast data:', error)
    throw error
  }
}