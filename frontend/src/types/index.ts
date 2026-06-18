export interface HealthResponse {
  status: string
  service: string
  version: string
  qdrant_connected: boolean
  auth_enabled: boolean
  client_host: string | null
}

export interface ReviewResponse {
  filename: string
  code_review: CodeReviewResult
  tutor_explanation: TutorResult
  rubric: RubricResult
  feedback: FeedbackResult
}

export interface CodeReviewResult {
  summary: string
  mistakes: string[]
  suggestions: string[]
  corrected_code: string | null
  filename_check: CheckResult | null
  structure_check: CheckResult | null
}

export interface CheckResult {
  passed: boolean
  message: string
}

export interface TutorResult {
  concepts_explained: string[]
  learning_resources: string[]
  misconceptions: string[]
}

export interface RubricResult {
  scores: Record<string, number>
  total_score: number
  max_score: number
  comments: string[]
}

export interface FeedbackResult {
  strengths: string[]
  improvements: string[]
  overall_comment: string
}

export interface KnowledgeStatsResponse {
  collections: Record<string, {
    points_count: number
    description: string
  }>
}

export interface KnowledgeSearchItem {
  id: string
  score: number
  text: string
  source: string
}

export interface KnowledgeSearchResponse {
  query: string
  collection: string
  results: KnowledgeSearchItem[]
}

export interface UploadResponse {
  filename: string
  review: {
    summary: string
    mistakes: string[]
    suggestions: string[]
  }
}

export type ReviewStatus = 'idle' | 'uploading' | 'reviewing' | 'done' | 'error'
