import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { Search } from '@/components/search'
import { ThemeSwitch } from '@/components/theme-switch'
import { ConfigDrawer } from '@/components/config-drawer'
import { TransactionHistory } from './components/transaction-history'

export function Transactions() {
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
        <div className='mb-6'>
          <h1 className='text-3xl font-bold tracking-tight'>Transactions</h1>
          <p className='text-muted-foreground'>
            View your transaction history and spending patterns powered by Plaid integration.
          </p>
        </div>
        
        <TransactionHistory />
      </Main>
    </>
  )
}