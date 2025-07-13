import React from "react";

const TopHeader = () => {
  return (
    <div className="fixed top-4 left-72 right-6 z-40">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-5 rounded-2xl shadow-xl flex items-center justify-between">
        {/* Left side: Title + subtitle */}
        <div>
          <h1 className="text-2xl font-bold">
            Natural Language Cross-Platform Data Query RAG Agent
          </h1>
          <p className="text-sm text-white/80 mt-1">
            Real-time insights for your wealth management firm
          </p>
        </div>

        {/* Right side: Stylized V icon */}
        <div className="w-10 h-10 flex items-center justify-center rounded-full bg-white text-blue-600 font-bold text-xl shadow-md">
          V
        </div>
      </div>
    </div>
  );
};

export default TopHeader; 