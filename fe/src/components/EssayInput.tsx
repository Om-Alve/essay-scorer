import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { Loader2, Upload } from "lucide-react";

interface EssayInputProps {
  onSubmit: (essay: string, topic: string) => void;
  isLoading: boolean;
}

export const EssayInput = ({ onSubmit, isLoading }: EssayInputProps) => {
  const [essay, setEssay] = useState("");
  const [topic, setTopic] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState("text");
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleTextSubmit = () => {
    if (!essay.trim() || !topic.trim()) {
      toast({
        title: "Missing Information",
        description: "Please provide both topic and essay text.",
        variant: "destructive",
      });
      return;
    }
    onSubmit(essay, topic);
  };

  const handleFileUpload = async () => {
    if (!file) {
      toast({
        title: "No File Selected",
        description: "Please select a PDF file to upload.",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/ocr-marathi-essay", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("OCR processing failed");
      }

      const data = await response.json();
      setEssay(data.essay);
      setTopic(data.topic);
      setActiveTab("text");

      toast({
        title: "Success",
        description: "Essay extracted from PDF successfully!",
      });
    } catch (error) {
      toast({
        title: "Upload Failed",
        description: "Failed to process PDF. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-8 py-12">
      <div className="bg-card rounded-3xl p-8 md:p-12 shadow-card border border-border">
        <div className="text-center mb-8">
          <Button
            variant="outline"
            className="rounded-full mb-4 px-6"
            onClick={() => window.location.reload()}
          >
            Review Your Essay
          </Button>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="text">Type Essay</TabsTrigger>
            <TabsTrigger value="upload">Upload PDF</TabsTrigger>
          </TabsList>

          <TabsContent value="text" className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="topic" className="text-base">
                Essay Topic
              </Label>
              <Input
                id="topic"
                placeholder="Enter the essay topic..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="rounded-2xl p-6 text-base"
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="essay" className="text-base">
                Essay Text
              </Label>
              <Textarea
                id="essay"
                placeholder="माझा आवडता छंद"
                value={essay}
                onChange={(e) => setEssay(e.target.value)}
                className="rounded-2xl p-6 min-h-[300px] text-base resize-none"
                disabled={isLoading}
              />
            </div>

            <Button
              onClick={handleTextSubmit}
              disabled={isLoading}
              className="w-full rounded-full py-6 text-lg shadow-button hover:shadow-lg transition-all"
              size="lg"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Grading...
                </>
              ) : (
                "Get Grade"
              )}
            </Button>
          </TabsContent>

          <TabsContent value="upload" className="space-y-6">
            <div className="space-y-4">
              <Label htmlFor="file-upload" className="text-base">
                Upload Marathi Essay PDF
              </Label>
              <div
                className="border-2 border-dashed border-border rounded-2xl p-12 text-center cursor-pointer hover:border-primary transition-colors"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground mb-2">
                  {file ? file.name : "Click to upload or drag and drop"}
                </p>
                <p className="text-sm text-muted-foreground">PDF files only</p>
              </div>
              <Input
                ref={fileInputRef}
                id="file-upload"
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
              />
            </div>

            <Button
              onClick={handleFileUpload}
              disabled={isProcessing || !file}
              className="w-full rounded-full py-6 text-lg shadow-button hover:shadow-lg transition-all"
              size="lg"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Processing...
                </>
              ) : (
                "Process PDF & Get Grade"
              )}
            </Button>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};
