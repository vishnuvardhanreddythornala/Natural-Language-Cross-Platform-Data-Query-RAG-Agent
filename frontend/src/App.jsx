import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import TopHeader from "./components/TopHeader"; 
import Dashboard from "./components/Dashboard";
import QueryInterface from "./components/QueryInterface";
import QueryHistory from "./components/QueryHistory";
import QueryProvider from "./contexts/QueryContext";

const App = () => {
  return (
    <QueryProvider>
      <Router>
        <div className="flex bg-[#0f172a] min-h-screen text-white">
          <Sidebar />
          <div className="ml-64 flex-1">
            <main className="relative">
              <Routes>
                {/*  Wrap TopHeader ONLY in this route */}
                <Route
                  path="/"
                  element={
                    <>
                      <TopHeader />
                      <div className="mt-36 px-6 pb-6">
                        <Dashboard />
                      </div>
                    </>
                  }
                />
                {/*  No TopHeader in these */}
                <Route path="/query-interface" element={<QueryInterface />} />
                <Route path="/query-history" element={<QueryHistory />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </QueryProvider>
  );
};

export default App;
