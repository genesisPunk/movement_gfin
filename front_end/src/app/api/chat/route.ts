import { google } from "@ai-sdk/google";
import { streamText } from "ai";
import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  try {
    console.log("ssup");
    const { messages, model, temperature, frequencyPenalty, presencePenalty } =
      await req.json();

    const result = await streamText({
      model: google("gemini-1.5-flash"),
      messages,
      temperature: temperature || 0.7,
      frequencyPenalty: frequencyPenalty || 0,
      presencePenalty: presencePenalty || 0,
    });

    return result.toDataStreamResponse();
  } catch (error) {
    console.error("Error in POST handler:", error);
    return new Response(
      JSON.stringify({ error: "Failed to process request" }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

export const config = {
  api: {
    bodyParser: false,
  },
};
