"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Camera, TrendingUp, Hand, Plane } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { MessageWindow } from "./MessageWindow";
import SentientIcon from "@/assets/SentientSvg";
import { useWallet } from "@razorlabs/razorkit";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog";
import SwapWidget from "@mosaicag/swap-widget";
import axios from "axios";

const suggestionCards = [
  {
    id: 1,
    icon: TrendingUp,
    title: "I want to 2x my money",
    subtitle: "High-growth investment strategies",
  },
  {
    id: 2,
    icon: Hand,
    title: "I want stable return like 2% monthly",
    subtitle: "Low-risk, steady investment options",
  },
  {
    id: 3,
    icon: Plane,
    title: "I want to retire early with passive income",
    subtitle: "Financial independence & wealth planning",
  },
];

export default function Playground() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedToken, setSelectedToken] = useState(null);
  const [tokens, setTokens] = useState([]);
  const [apps, setApps] = useState([]);

  const messagesEndRef = useRef(null);
  const wallet = useWallet();

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    setIsLoading(true);
    setHasSubmitted(true);

    setMessages((prev) => [...prev, { role: "user", content: input }]);

    try {
      const response = await axios.post("http://localhost:8001/submit_goal", {
        user_goal: input,
      });

      const { analysis, recommendations } = response.data;

      const tokens = analysis.map((item) => {
        const eventTitle =
          item.sentiment.key_events && item.sentiment.key_events[0]
            ? item.sentiment.key_events[0].title
            : "";

        return {
          symbol: item.symbol,
          analysis: eventTitle,
          overall: item.sentiment.sentiment,
          price: item.market.current_price,
        };
      });
      const lastThreeTokens = tokens.slice(0, 3);

      setTokens(lastThreeTokens);

      const applications = Object.values(analysis[0].applications || {}).flat();
      const appNames = applications.slice(0, 3).map((app) => {
        return {
          name: app?.name || "",
          link: app?.link || "",
          desc: app?.description || "",
        };
      });
      setApps(appNames);
      setInput("");

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: recommendations,
        },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Something went wrong. Please try again." },
      ]);
    }

    setIsLoading(false);
  };

  const openModal = (token) => {
    setSelectedToken(token);
    setIsModalOpen(true);
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-auto p-4 pt-14">
        {messages.length === 0 ? (
          <div className="text-center mb-16">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <SentientIcon />
            </div>
            <h1 className="text-2xl font-semibold mb-2">Hola, Amigos</h1>
            <h2 className="text-xl font-medium mb-3">
              Can I help you with anything?
            </h2>
            <p className="text-muted-foreground text-sm max-w-md mx-auto">
              Ready to assist you with anything you need: from answering
              questions to providing recommendations. Let’s get started!
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-12">
              {suggestionCards.map((card) => (
                <Card
                  key={card.id}
                  className="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => setInput(card.title)}
                >
                  <div className="bg-gray-900 w-10 h-10 rounded-lg flex items-center justify-center mb-3">
                    <card.icon className="w-5 h-5 text-white" />
                  </div>
                  <h3 className="font-medium text-sm mb-1">{card.title}</h3>
                  <p className="text-xs text-muted-foreground">
                    {card.subtitle}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        ) : (
          <div>
            <MessageWindow messages={messages} isLoading={isLoading} />
            {tokens.length > 0 && (
              <div className="relative mt-2 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-violet-500/10 via-fuchsia-500/10 to-violet-500/10 " />
                <div className="relative bg-black/95  rounded-xl border border-white/10">
                  <div className="p-6">
                    <h3 className="text-lg font-medium bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent mb-4">
                      Market Intelligence & Strategy Recommendations
                    </h3>
                    <div className="grid lg:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <h4 className="text-md font-medium text-gray-400 flex items-center gap-2">
                          <TrendingUp className="w-4 h-4 text-violet-400" />
                          Token Opportunities
                        </h4>
                        {tokens.map((token, index) => (
                          <Card
                            key={index}
                            className="bg-white/5 border-0 hover:bg-white/10 transition-all duration-200 group"
                          >
                            <div className="p-4">
                              <div className="flex justify-between items-center mb-3">
                                <span className="font-bold text-white">
                                  {token.symbol}
                                </span>
                                <Button
                                  onClick={() => openModal(token)}
                                  size="lg"
                                  className="bg-gradient-to-r from-violet-500 to-fuchsia-500 hover:from-violet-600 hover:to-fuchsia-600 border-0 text-white"
                                >
                                  Buy
                                </Button>
                              </div>
                              <div className="grid gap-2 text-sm">
                                <p className="text-gray-400 line-clamp-2">
                                  {token.analysis}
                                </p>
                                <div className="flex justify-between items-center">
                                  <span
                                    className={`px-2 py-0.5 rounded-full text-xs ${
                                      token.overall === "bullish"
                                        ? "bg-green-500/20 text-green-400"
                                        : "bg-yellow-500/20 text-yellow-400"
                                    }`}
                                  >
                                    {token.overall}
                                  </span>
                                  <span className="font-medium text-white">
                                    Current Price : {token.price}
                                  </span>
                                </div>
                              </div>
                            </div>
                          </Card>
                        ))}
                      </div>

                      <div className="space-y-4">
                        <h4 className="text-md font-medium text-gray-400 flex items-center gap-2">
                          <Plane className="w-4 h-4 text-fuchsia-400" />
                          Recommended Platforms
                        </h4>
                        <div className="grid gap-2">
                          {apps.map((app, index) => (
                            <Card
                              key={index}
                              className="bg-white/5 border-0 hover:bg-white/10 transition-all duration-200"
                            >
                              <div className="p-4 flex justify-between items-center">
                                <span className="text-white font-medium">
                                  {app.name}
                                </span>
                                <Button
                                  size="lg"
                                  className="bg-gradient-to-r from-violet-500 to-fuchsia-500 hover:from-violet-600 hover:to-fuchsia-600 border-0 text-white"
                                >
                                  <a
                                    href={app.link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    Execute Task
                                  </a>{" "}
                                </Button>
                              </div>

                              <div className="p-4">
                                <p className="text-gray-400 line-clamp-2">
                                  {app.desc}
                                </p>
                              </div>
                            </Card>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      <form
        onSubmit={handleFormSubmit}
        className="p-4 border-t bg-white sticky bottom-0 w-full"
      >
        <div className="flex gap-2">
          <Button variant="outline" size="icon">
            <Camera className="w-4 h-4" />
          </Button>
          <div className="flex-1 relative">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              className="pr-20 bg-white"
              disabled={isLoading}
            />
            <Button
              type="submit"
              disabled={isLoading}
              className="absolute right-1 top-0"
            >
              Send <Send className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
      </form>
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Swap {selectedToken?.symbol}</DialogTitle>
          </DialogHeader>
          <div className="Mosaic">
            <SwapWidget wallet={wallet} apiKey="..." />
          </div>
          <DialogClose asChild>
            <Button className="mt-4 w-full">Close</Button>
          </DialogClose>
        </DialogContent>
      </Dialog>
    </div>
  );
}
