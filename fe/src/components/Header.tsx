import { Button } from "@/components/ui/button";

export const Header = () => {
  return (
    <header className="w-full py-6 px-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="text-2xl font-bold text-foreground">
          स्कोर.ai
        </div>
        <Button variant="default" size="lg" className="rounded-full px-6">
          Get Started
        </Button>
      </div>
    </header>
  );
};
