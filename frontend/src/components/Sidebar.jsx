import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import { Home, Search, BarChart2, ChevronLeft, ChevronRight } from "lucide-react";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <aside
      className={`fixed top-0 left-0 h-screen ${
        isOpen ? "w-64" : "w-16"
      } bg-slate-800 text-white p-4 shadow-lg z-50 transition-all duration-300`}
    >
      {/*  Toggle button only */}
      <div className="flex justify-end mb-8">
        <button onClick={toggleSidebar} className="text-slate-300 hover:text-white">
          {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
        </button>
      </div>

      {/*  Navigation Links */}
      <nav className="flex flex-col gap-4">
        <SidebarLink to="/" icon={<Home size={18} />} label="Dashboard" isOpen={isOpen} />
        <SidebarLink to="/query-interface" icon={<Search size={18} />} label="Query Interface" isOpen={isOpen} />
        <SidebarLink to="/query-history" icon={<BarChart2 size={18} />} label="Query History" isOpen={isOpen} />
      </nav>
    </aside>
  );
};

const SidebarLink = ({ to, icon, label, isOpen }) => {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 px-3 py-2 rounded-lg transition font-medium ${
          isActive
            ? "bg-blue-600 text-white"
            : "text-slate-300 hover:bg-slate-800 hover:text-white"
        }`
      }
    >
      {icon}
      {isOpen && <span>{label}</span>}
    </NavLink>
  );
};

export default Sidebar;
