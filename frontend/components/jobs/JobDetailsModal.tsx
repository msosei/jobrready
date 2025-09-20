import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';
import { MapPin, DollarSign, Clock, Building2, Bookmark, Share2, Heart } from 'lucide-react';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  type: string;
  remote: boolean;
  urgent: boolean;
  posted: string;
  isNew: boolean;
  description: string;
  requirements?: string[];
  benefits?: string[];
}

interface JobDetailsModalProps {
  job: Job;
  isOpen: boolean;
  onClose: () => void;
}

export default function JobDetailsModal({ job, isOpen, onClose }: JobDetailsModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader className="space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <DialogTitle className="text-2xl mb-2">{job.title}</DialogTitle>
              <div className="flex items-center gap-2 text-lg text-muted-foreground mb-3">
                <Building2 className="h-5 w-5" />
                {job.company}
              </div>
            </div>
            <div className="flex gap-2">
              {job.isNew && (
                <Badge variant="secondary" className="bg-green-100 text-green-700">
                  NEW
                </Badge>
              )}
              {job.urgent && (
                <Badge variant="destructive">
                  URGENT
                </Badge>
              )}
            </div>
          </div>

          <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
            <div className="flex items-center">
              <MapPin className="h-4 w-4 mr-2" />
              {job.location}
            </div>
            <div className="flex items-center">
              <DollarSign className="h-4 w-4 mr-2" />
              {job.salary}
            </div>
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              {job.posted}
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {job.remote && <Badge variant="outline">Remote</Badge>}
            <Badge variant="outline">{job.type}</Badge>
          </div>

          <div className="flex gap-3">
            <Button className="flex-1">Apply Now</Button>
            <Button variant="outline" size="icon">
              <Bookmark className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon">
              <Share2 className="h-4 w-4" />
            </Button>
          </div>
        </DialogHeader>

        <Separator />

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3">Job Description</h3>
            <p className="text-muted-foreground leading-relaxed">
              {job.description}
            </p>
          </div>

          {job.requirements && (
            <div>
              <h3 className="text-lg font-semibold mb-3">Requirements</h3>
              <ul className="space-y-2">
                {job.requirements.map((req, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-primary mr-2">•</span>
                    <span className="text-muted-foreground">{req}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {job.benefits && (
            <div>
              <h3 className="text-lg font-semibold mb-3">Benefits</h3>
              <div className="grid grid-cols-2 gap-2">
                {job.benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    <span className="text-muted-foreground">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div>
            <h3 className="text-lg font-semibold mb-3">About {job.company}</h3>
            <p className="text-muted-foreground">
              {job.company} is a leading technology company focused on innovation and growth. 
              We pride ourselves on creating an inclusive workplace where talented individuals 
              can thrive and make a meaningful impact.
            </p>
          </div>
        </div>

        <Separator />

        <div className="flex gap-3">
          <Button className="flex-1">Apply Now</Button>
          <Button variant="outline">Save Job</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
