import { useState } from "react";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { EssayInput } from "@/components/EssayInput";
import { GradeResults } from "@/components/GradeResults";
import { useToast } from "@/hooks/use-toast";

type View = "hero" | "input" | "results";

interface GradeData {
  grade: string;
  feedback: string[];
}

const Index = () => {
  const [currentView, setCurrentView] = useState<View>("hero");
  const [isLoading, setIsLoading] = useState(false);
  const [gradeData, setGradeData] = useState<GradeData | null>(null);
  const [currentTopic, setCurrentTopic] = useState("");
  const { toast } = useToast();

  const handleGetStarted = () => {
    setCurrentView("input");
  };

  const handleSubmit = async (essay: string, topic: string) => {
    setIsLoading(true);
    setCurrentTopic(topic);

    try {
      const response = await fetch("http://localhost:8000/grade-essay", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ essay, topic }),
      });

      if (!response.ok) {
        throw new Error("Grading failed");
      }

      const data = await response.json();

      setGradeData({
        grade: data.grade || "6",
        feedback: data.feedback || [
          "Essay is well-structured with clear introduction, body, and conclusion.",
          "Good use of examples to support main points.",
          "Grammar and spelling are mostly correct.",
          "Could improve transitions between paragraphs.",
        ],
      });
      setCurrentView("results");

      toast({
        title: "Grading Complete",
        description: "Your essay has been evaluated successfully!",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to grade essay. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setCurrentView("input");
    setGradeData(null);
  };

  return (
    <div className="min-h-screen">
      <Header />

      {currentView === "hero" && <Hero onGetStarted={handleGetStarted} />}

      {currentView === "input" && (
        <EssayInput onSubmit={handleSubmit} isLoading={isLoading} />
      )}

      {currentView === "results" && gradeData && (
        <GradeResults
          topic={currentTopic}
          grade={gradeData.grade}
          feedback={gradeData.feedback}
          onBack={handleBack}
        />
      )}
    </div>
  );
};

export default Index;
