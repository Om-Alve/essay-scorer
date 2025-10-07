import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface GradeResultsProps {
  topic: string;
  grade: string;
  feedback: string[];
  onBack: () => void;
}

export const GradeResults = ({ topic, grade, feedback, onBack }: GradeResultsProps) => {
  return (
    <div className="w-full max-w-5xl mx-auto px-8 py-12">
      <div className="flex items-start justify-between mb-8">
        <div>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
            {topic}
          </h2>
        </div>
        <Badge 
          variant="secondary" 
          className="text-xl px-6 py-2 rounded-2xl bg-accent text-accent-foreground shadow-card"
        >
          Grade {grade}
        </Badge>
      </div>

      <div className="bg-card rounded-3xl p-8 md:p-12 shadow-card border border-border">
        <h3 className="text-2xl font-semibold mb-6 text-foreground">Feedback</h3>
        
        <ul className="space-y-4">
          {feedback.map((item, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="text-muted-foreground mt-1">•</span>
              <span className="text-foreground leading-relaxed flex-1">{item}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-8 flex justify-center">
        <Button
          onClick={onBack}
          variant="outline"
          size="lg"
          className="rounded-full px-12 shadow-button hover:shadow-lg transition-all"
        >
          Grade Another Essay
        </Button>
      </div>
    </div>
  );
};
