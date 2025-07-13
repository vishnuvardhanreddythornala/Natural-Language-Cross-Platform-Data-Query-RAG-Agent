/* eslint-disable react-refresh/only-export-components */

import React, { createContext, useState } from "react";

export const QueryContext = createContext();

const QueryProvider = ({ children }) => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [graphData, setGraphData] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [activeTab, setActiveTab] = useState("text");

  return (
    <QueryContext.Provider value={{ question, setQuestion, response, setResponse, graphData, setGraphData, tableData, setTableData,activeTab,
        setActiveTab, }}>
      {children}
    </QueryContext.Provider>
  );
};

export default QueryProvider;
