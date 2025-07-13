import React, { useState, useEffect } from "react";
import { Line, Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch("http://localhost:8000/dashboard-metrics");
        const data = await res.json();
        setMetrics(data);
      } catch (error) {
        console.error("Error fetching metrics:", error);
      }
    };
    fetchMetrics();
  }, []);

  //  Line Chart data (Portfolio Growth)
  const lineData = {
    labels: metrics?.portfolio_growth?.map((item) => item.month) || [],
    datasets: [
      {
        label: "Portfolio Growth (Cr)",
        data: metrics?.portfolio_growth?.map((item) => item.value) || [],
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,0.3)",
        fill: true,
      },
    ],
  };

  //  Pie Chart data (Asset Allocation)
  const pieData = {
    labels: metrics?.asset_allocation?.map((item) => item.asset) || [],
    datasets: [
      {
        data: metrics?.asset_allocation?.map((item) => item.percent) || [],
        backgroundColor: ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"],
      },
    ],
  };

  //  Bar Chart data (Top Relationship Managers)
  const barData = {
    labels: metrics?.rm_clients?.map((item) => item.rm) || [],
    datasets: [
      {
        label: "Clients Managed",
        data: metrics?.rm_clients?.map((item) => item.clients) || [],
        backgroundColor: "#6366f1",
      },
    ],
  };

  return (
    <div className="min-h-screen w-full bg-slate-900 text-white px-8 py-6">
      {/*  Header */}
      <div className="mb-6 pt-4">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Welcome to the Dashboard!</h1>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard title="Top Portfolios" value={metrics?.top_portfolios ?? "..."} />
        <StatCard title="Total AUM" value={metrics?.total_aum ?? "..."} color="green" />
        <StatCard title="Active RMs" value={metrics?.active_rms ?? "..."} />
        <StatCard title="High Risk" value={metrics?.high_risk ?? "..."} color="red" />
      </div>

      {/*  Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        {/* Line Chart */}
        <div className="bg-slate-800 p-4 rounded-xl shadow">
          <h2 className="text-lg font-semibold mb-4 text-white">Portfolio Growth Trend</h2>
          <Line data={lineData} />
        </div>

        {/* Pie Chart */}
        <div className="bg-slate-800 p-4 rounded-xl shadow">
          <h2 className="text-lg font-semibold mb-4 text-white">Asset Allocation</h2>
          <Pie data={pieData} />
        </div>

        {/* Bar Chart */}
        <div className="bg-slate-800 p-4 rounded-xl shadow md:col-span-2">
          <h2 className="text-lg font-semibold mb-4 text-white">Top Relationship Managers</h2>
          <Bar data={barData} />
        </div>
      </div>
    </div>
  );
};

// Stat Card Component
const StatCard = ({ title, value, color }) => {
  const valueClass =
    color === "green"
      ? "text-green-400"
      : color === "red"
      ? "text-red-400"
      : "text-blue-400";

  return (
    <div className="bg-slate-800 p-4 rounded-xl shadow hover:shadow-md transition">
      <div className="font-medium text-slate-400">{title}</div>
      <div className={`text-2xl font-bold ${valueClass}`}>{value}</div>
    </div>
  );
};

export default Dashboard;
3