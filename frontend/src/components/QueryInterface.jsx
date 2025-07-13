import React, { useContext, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Mic, Send } from "lucide-react";
import { QueryContext } from "../contexts/QueryContext";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const QueryInterface = () => {
  const {
    question,
    setQuestion,
    response,
    setResponse,
    graphData,
    setGraphData,
    tableData,
    setTableData,
    activeTab,
    setActiveTab,
  } = useContext(QueryContext);

  const [showSamples, setShowSamples] = useState(true);
  const [loading, setLoading] = useState(false); // spinner state

  const sampleQuestions = [
    "What are the top five portfolios?",
    "List clients who prefer investing in Real Estate.",
    "Give me the breakup of portfolio values per relationship manager.",
    "Who are the top relationship managers by portfolio?",
  ];

  const handleSampleClick = (sample) => {
    setQuestion(sample);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setResponse(data.response);
      setGraphData(data.graph_data);
      setTableData(data.table_data);
      setActiveTab("text");
      setShowSamples(false);
    } catch (error) {
      console.error("Error querying:", error);
    } finally {
      setLoading(false);
    }
  };

  const barChartData = {
    labels: graphData.map((item) => item.label),
    datasets: [
      {
        label: "Value",
        data: graphData.map((item) => item.value),
        backgroundColor: "#3b82f6",
      },
    ],
  };

  return (
    <div className="pt-16 px-8 pb-8 min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <div className="mb-14 text-center">
        <div className="flex justify-center items-center gap-2 mb-1">
          <h1 className="text-3xl font-bold">⚡AI-Powered Query Interface</h1>
        </div>
        <p className="text-slate-400 text-sm">
          Natural language queries for intelligent portfolio analysis
        </p>
      </div>

      {/* Input Box */}
      <form
        onSubmit={handleSubmit}
        className="bg-slate-800 rounded-xl p-4 flex items-center gap-3 mb-6"
      >
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask me anything about your portfolios, clients, or transactions..."
          className="flex-1 bg-transparent text-white resize-none focus:outline-none h-20"
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />

        <button
          type="button"
          className="p-2 hover:bg-slate-700 rounded-full"
          title="Voice (not implemented)"
        >
          <Mic className="text-slate-400" />
        </button>

        <button
          type="submit"
          className="p-2 bg-blue-600 hover:bg-blue-700 rounded-full"
          title="Submit"
        >
          <Send className="text-white" />
        </button>

        {loading && (
          <div className="ml-2">
            <div className="w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
      </form>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6">
        {["text", "table", "graph"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              activeTab === tab
                ? "bg-blue-600 text-white"
                : "bg-slate-700 text-slate-300 hover:bg-slate-600"
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Sample Questions BELOW tabs */}
      {showSamples && (
        <div className="bg-slate-800 p-4 rounded-xl mb-6">
          <h2 className="text-lg font-semibold mb-4">💡 Sample Questions</h2>
          <div className="flex flex-col gap-3">
            {sampleQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSampleClick(q)}
                className="w-full text-left bg-slate-700 hover:bg-blue-600 text-slate-200 hover:text-white px-4 py-2 rounded-lg transition-all duration-200 shadow hover:shadow-md transform hover:scale-[1.02] active:scale-100"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Text Response */}
      {activeTab === "text" && response && (
        <div className="mb-6 p-4 bg-slate-800 rounded-xl shadow">
          <h2 className="text-lg font-semibold mb-2">Response</h2>
          <p className="text-slate-300 whitespace-pre-line">{response}</p>
        </div>
      )}

      {/* Table Response */}
      {activeTab === "table" && tableData.length > 0 && (
        <div className="p-4 bg-slate-800 rounded-xl shadow overflow-x-auto">
          <h2 className="text-lg font-semibold mb-4">Table</h2>
          <table className="min-w-full text-sm text-left text-slate-300">
            <thead className="text-xs uppercase text-slate-400 border-b border-slate-600">
              <tr>
                <th className="px-6 py-3">Client</th>
                <th className="px-6 py-3">Portfolio Value</th>
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, idx) => (
                <tr
                  key={idx}
                  className="border-b border-slate-700 hover:bg-slate-700"
                >
                  <td className="px-6 py-4">{row.client}</td>
                  <td className="px-6 py-4">{row.portfolio_value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Graph Response */}
      {activeTab === "graph" && graphData.length > 0 && (
        <div className="mb-6 p-4 bg-slate-800 rounded-xl shadow">
          <h2 className="text-lg font-semibold mb-4">Graph</h2>
          <Bar data={barChartData} />
        </div>
      )}
    </div>
  );
};

export default QueryInterface;
