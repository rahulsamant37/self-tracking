import { Route, Routes } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Dsa } from './pages/Dsa'
import { Goals } from './pages/Goals'
import { Today } from './pages/Today'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="today" element={<Today />} />
        <Route path="dsa" element={<Dsa />} />
        <Route path="goals" element={<Goals />} />
      </Route>
    </Routes>
  )
}
