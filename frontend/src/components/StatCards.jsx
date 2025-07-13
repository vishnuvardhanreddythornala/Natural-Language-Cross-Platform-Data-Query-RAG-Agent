// src/components/StatCard.jsx
import React from "react";

const StatCard = ({ title, value }) => {
  return (
    <div className="bg-white rounded-2xl shadow-md p-4 w-full md:w-60">
      <h2 className="text-gray-500 text-sm font-medium">{title}</h2>
      <p className="text-2xl font-semibold text-gray-800">{value}</p>
    </div>
  );
};

export default StatCard;
