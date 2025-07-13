// src/components/GraphView.jsx
import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

const GraphView = ({ data }) => {
  if (!data || data.length === 0) return <p>No data to display.</p>;

  const chartData = {
    labels: data.map((item) => item.label),
    datasets: [
      {
        label: "Value",
        data: data.map((item) => item.value),
        backgroundColor: "#3b82f6",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Sample Bar Chart" },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default GraphView;
