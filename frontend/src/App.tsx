import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { ReviewPage } from './pages/ReviewPage'
import { KnowledgePage } from './pages/KnowledgePage'

export default function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            borderRadius: '12px',
            padding: '12px 16px',
            fontSize: '14px',
            background: 'var(--color-surface)',
            color: 'var(--color-text)',
            border: '1px solid var(--color-border)',
          },
        }}
      />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/review" element={<ReviewPage />} />
          <Route path="/knowledge" element={<KnowledgePage />} />
          <Route path="/docs" element={<Navigate to="/api/docs" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
