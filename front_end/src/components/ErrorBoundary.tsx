"use client";
import React, { ReactNode, useState, ReactElement } from "react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { AlertCircle } from "lucide-react";

interface Props {
  children: ReactNode;
}

const ErrorBoundary: React.FC<Props> = ({ children }) => {
  const [hasError, setHasError] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const resetError = () => {
    setHasError(false);
    setError(null);
  };

  const handleError = (error: Error) => {
    console.error("Uncaught error:", error);
    setHasError(true);
    setError(error);
  };

  return (
    <>
      {hasError ? (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>
            {error?.message}
            <Button variant="outline" onClick={resetError} className="mt-4">
              Try again
            </Button>
          </AlertDescription>
        </Alert>
      ) : (
        children
      )}
    </>
  );
};

const withErrorBoundary =
  (Component: React.ComponentType) =>
  (props: any): ReactElement => {
    return (
      <ErrorBoundary>
        <Component {...props} />
      </ErrorBoundary>
    );
  };

export default withErrorBoundary;
