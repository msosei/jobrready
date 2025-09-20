import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { AI } from '@/lib/ai'

export default function PortfolioProjects() {
  const [projects, setProjects] = useState<any[]>([])
  const [generating, setGenerating] = useState(false)

  async function generateProject() {
    setGenerating(true)
    try {
      const { success, data } = await AI.portfolioProject({ skills: ['React', 'Node.js', 'TypeScript'], experience: 'intermediate', userId: 'user-123' })
      if (success && data) setProjects(prev => [...prev, data])
    } catch (e) {
      console.error('Failed to generate project')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Projects & Portfolio</CardTitle>
        <CardDescription>
          Generate project ideas and starter code repositories
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Button onClick={generateProject} disabled={generating}>
            {generating ? 'Generating...' : 'Generate Project Idea'}
          </Button>
          {projects.length > 0 && (
            <div className="space-y-2">
              {projects.map((project, i) => (
                <div key={i} className="p-4 border rounded">
                  <h4 className="font-medium">{project.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{project.description}</p>
                  <div className="flex gap-2 mt-2">
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {project.techStack?.join(', ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
