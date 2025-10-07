import { Button } from "@/components/ui/button";

interface HeroProps {
  onGetStarted: () => void;
}

export const Hero = ({ onGetStarted }: HeroProps) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-8 text-center">
      <div className="mb-8 px-8 py-3 bg-card/80 backdrop-blur-sm rounded-full border border-border shadow-card">
        <p className="text-sm md:text-base text-foreground">
          तत्काल निबंध स्कोरे. वास्तविक शिक्षण अंतर्दृष्टि.
        </p>
      </div>
      
      <h1 className="text-5xl md:text-7xl font-bold mb-6 text-foreground">
        Grade <span className="italic">Smarter</span>, Not Harder.
      </h1>
      
      <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mb-12 leading-relaxed">
        Harness the power of AI to evaluate essays instantly — with detailed feedback on grammar,
        coherence, and argument quality. Save hours while ensuring fair, consistent, and insightful grading.
      </p>
      
      <Button 
        onClick={onGetStarted}
        size="lg" 
        className="rounded-full px-12 py-6 text-lg shadow-button hover:shadow-lg transition-all"
      >
        Upload Your Essay
      </Button>
    </div>
  );
};
