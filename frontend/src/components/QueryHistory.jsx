import React, { useEffect, useState } from "react";
import { Clock, Trash, Download, CalendarDays } from "lucide-react";

const QueryHistory = () => {
  const [recentQueries, setRecentQueries] = useState([]);
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  const fetchQueries = async () => {
    try {
      const res = await fetch("http://localhost:8000/recent-queries");
      const data = await res.json();
      setRecentQueries(data.queries);
    } catch (error) {
      console.error("Error fetching recent queries:", error);
    }
  };

  useEffect(() => {
    fetchQueries();
  }, []);

  const handleDelete = async (index) => {
    try {
      await fetch(`http://localhost:8000/recent-queries/${index}`, {
        method: "DELETE",
      });
      fetchQueries();
    } catch (error) {
      console.error("Error deleting query:", error);
    }
  };

  const handleExport = () => {
    window.open("http://localhost:8000/recent-queries/export", "_blank");
  };

  const handleFilter = async () => {
    if (!fromDate || !toDate) return;
    try {
      const res = await fetch(
        `http://localhost:8000/recent-queries/filter?start=${fromDate}&end=${toDate}`
      );
      const data = await res.json();
      setRecentQueries(data.queries);
    } catch (error) {
      console.error("Error filtering queries:", error);
    }
  };

  return (
    <div className="p-6 bg-slate-900 min-h-screen text-white">
      {/*  Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Clock size={22} className="text-blue-400" />
          Recent Queries
        </h1>
        <p className="text-slate-400 text-sm">
          A history of your previously asked questions
        </p>
      </div>

      {/* Filter + Export */}
      <div className="flex flex-wrap gap-4 mb-4 items-center">
        <div className="flex gap-2 items-center">
          <CalendarDays size={18} />
          <input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
            className="px-3 py-1 rounded bg-slate-800 text-white border border-slate-700"
          />
          <span>to</span>
          <input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
            className="px-3 py-1 rounded bg-slate-800 text-white border border-slate-700"
          />
          <button
            onClick={handleFilter}
            className="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-sm"
          >
            Filter
          </button>
        </div>
        <div className="flex gap-3 ml-auto">
          <button
            onClick={handleExport}
            className="bg-green-600 hover:bg-green-700 px-3 py-1 rounded text-sm flex items-center gap-1"
          >
            <Download size={16} />
            Export CSV
          </button>
        </div>
      </div>

      {/*  Query List */}
      {recentQueries.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-400">
          <img
            src="/no-queries.svg"
            alt="No Queries"
            className="w-40 h-40 opacity-70 mb-4"
          />
          <p className="italic">No recent queries yet.</p>
        </div>
      ) : (
        <div className="bg-slate-800 rounded-xl shadow divide-y divide-slate-700 max-h-[500px] overflow-y-auto">
          {recentQueries.map((q, idx) => (
            <div
              key={idx}
              className="flex justify-between items-center py-3 px-4 hover:bg-slate-700 transition"
            >
              <div>
                <div className="text-white">{q.text}</div>
                <div className="text-xs text-slate-400">{q.time}</div>
              </div>
              <Trash
                size={18}
                className="text-red-400 hover:text-red-600 cursor-pointer"
                onClick={() => handleDelete(idx)}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QueryHistory;
