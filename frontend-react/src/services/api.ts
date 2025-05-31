export interface BotResponse {
  message: string;
  timestamp: Date;
}

// Simulates sending a message to a backend API
export const sendMessageToBackend = async (userMessage: string): Promise<BotResponse> => {
  console.log(`Simulating API call with message: "${userMessage}"`);

  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Simulate a response from the backend
  const botResponse: BotResponse = {
    message: `Backend echo: "${userMessage}" (This is a mock response)`,
    timestamp: new Date(),
  };

  console.log("Simulated API call finished, returning mock response:", botResponse);
  return botResponse;
};

// Example of a more complex API call structure if needed in the future
/*
interface AnalysisPayload {
  text: string;
  type: 'idea' | 'feedback';
}

interface AnalysisResult {
  id: string;
  summary: string;
  keywords: string[];
}

export const analyzeText = async (payload: AnalysisPayload): Promise<AnalysisResult> => {
  console.log("Simulating text analysis API call:", payload);
  await new Promise(resolve => setTimeout(resolve, 1500));
  const result: AnalysisResult = {
    id: Date.now().toString(),
    summary: `Mock analysis summary for: ${payload.text.substring(0, 30)}...`,
    keywords: ['mock', 'analysis', payload.type],
  };
  console.log("Simulated text analysis finished:", result);
  return result;
};
*/
