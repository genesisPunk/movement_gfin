"use client";

import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement
);

interface CoinStoreEntry {
  type: string;
  data?: {
    coin?: {
      value?: string;
    };
  };
}

import { useSearchParams } from "next/navigation";

export default function AddressPage() {
  const [loading, setLoading] = useState(true);
  const [tokenData, setTokenData] = useState<
    { tokenName: string; balance: number }[]
  >([]);
  const [trendData, setTrendData] = useState<{ day: string; value: number }[]>(
    []
  );

  const searchParams = useSearchParams();
  const address = searchParams.get("address");

  const fetchTokenData = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `https://aptos.testnet.porto.movementlabs.xyz/v1/accounts/${address}/resources`
      );

      const data = await response.json();
      // Filter only "0x1::coin::CoinStore"
      const filteredData = data.filter((entry: CoinStoreEntry) =>
        entry.type.startsWith("0x1::coin::CoinStore")
      );

      console.log(filteredData);

      // Extract token name, address & balance data
      const dataFormatted = filteredData
        .map((entry: CoinStoreEntry) => {
          let tokenName = null;

          // Check if it's AptosCoin separately
          if (entry.type.includes("aptos_coin::AptosCoin")) {
            tokenName = "Move"; // Rename AptosCoin to "Move"
          } else {
            // Extract token names from other tokens
            const match = entry.type.match(
              /CoinStore<[^:]+::(?:tokens::)?([\w]+)>/
            );
            if (match) {
              tokenName = match[1];
            }
          }

          if (tokenName) {
            return {
              tokenName,
              balance: (Number(entry.data?.coin?.value) || 0) / 1e8 || 0,
            };
          }

          return null;
        })
        .filter(Boolean);

      console.log(dataFormatted);
      return dataFormatted;
    } catch (error) {
      console.error("Error fetching data:", error);
      return [];
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchInfo = async () => {
      const fetchedTokenData = await fetchTokenData();
      // Add "MOVE" token data (if available)
      //   const chartData = { tokenName: "MOVE", balance: Number(balance) / 1e8 }; // Convert balance

      const combinedData: { tokenName: string; balance: number }[] = [
        ...fetchedTokenData,
        // chartData,
      ];

      setTokenData(combinedData);

      // Mock trend data for the last 7 days
      const mockTrendData = [
        { day: "Day 1", value: 1000 },
        { day: "Day 2", value: 1050 },
        { day: "Day 3", value: 1100 },
        { day: "Day 4", value: 1050 },
        { day: "Day 5", value: 1140 },
        { day: "Day 6", value: 1250 },
        { day: "Day 7", value: 1270 },
      ];
      setTrendData(mockTrendData);
    };

    fetchInfo();
  }, [address]);

  // Generate Pie Chart Data
  const pieChartData = {
    labels: tokenData.map((t) => `${t.tokenName} ${t.balance}`),
    datasets: [
      {
        data: tokenData.map((t) => t.balance),
        backgroundColor: [
          "#6C5CE7", // Purple
          "#00B894", // Teal
          "#0984E3", // Blue
          "#00CEC9", // Cyan
          "#FD79A8", // Pink
        ],
        hoverBackgroundColor: [
          "#6C5CE7", // Purple
          "#00B894", // Teal
          "#0984E3", // Blue
          "#00CEC9", // Cyan
          "#FD79A8", // Pink
        ],
      },
    ],
  };

  // Generate Line Chart Data for 7-Day Trend
  const lineChartData = {
    labels: trendData.map((item) => item.day),
    datasets: [
      {
        label: "Portfolio Value",
        data: trendData.map((item) => item.value),
        borderColor: "#0984E3", // Blue line color
        backgroundColor: "rgba(9, 132, 227, 0.2)", // Light Blue background
        fill: true,
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="p-4 space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {/* Pie Chart Card */}
        <Card>
          <CardHeader>
            <CardTitle>Token Distribution</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center items-center">
            {loading ? (
              <p>Loading token data...</p>
            ) : tokenData.length > 0 ? (
              <div className="w-full h-[310px] md:h-[400px]">
                {" "}
                {/* Full width, fixed height */}
                <Pie data={pieChartData} />
              </div>
            ) : (
              <p>No token data available.</p>
            )}
          </CardContent>
        </Card>

        {/* 7-Day Portfolio Trend Card */}
        <Card>
          <CardHeader>
            <CardTitle>7-Day Portfolio Trend</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center items-center">
            {loading ? (
              <p>Loading trend data...</p>
            ) : trendData.length > 0 ? (
              <div className="w-full h-[240px] md:h-[400px]">
                {" "}
                {/* Full width, fixed height */}
                <Line
                  data={lineChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: true,
                  }}
                />
                <h2 className="text-lg font-semibold text-center text-gray-700 mt-4">
                  Gfin will show the portfolio trend for last 7 days here
                </h2>
              </div>
            ) : (
              <p>No trend data available.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
